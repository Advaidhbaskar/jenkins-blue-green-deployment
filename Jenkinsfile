
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'advaidhb/blue-green-deployment'
        GIT_URL = 'https://github.com/Advaidhbaskar/jenkins-blue-green-deployment.git'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GIT_URL}"
            }
        }

        stage('Detect Active Environment') {
            steps {
                script {
                    def active = bat(
                        returnStdout: true,
                        script: '@kubectl get service blue-green-service -o jsonpath={.spec.selector.version}'
                    ).trim()

                    echo "Currently active environment: ${active}"

                    if (active == 'blue') {
                        env.TARGET = 'green'
                        env.TARGET_VERSION = '2.0'
                        env.TARGET_COLOR = 'Green'
                    } else if (active == 'green') {
                        env.TARGET = 'blue'
                        env.TARGET_VERSION = '1.0'
                        env.TARGET_COLOR = 'Blue'
                    } else {
                        error("Unknown active environment: ${active}")
                    }

                    echo "Deploying to inactive environment: ${env.TARGET}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-bluegreen-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat 'powershell -NoProfile -Command "$env:DOCKER_PASS | docker login --username $env:DOCKER_USER --password-stdin"'
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                }
            }
        }

        stage('Deploy to Inactive Environment') {
            steps {
                bat 'kubectl set image deployment/flask-%TARGET% flask-container=%IMAGE_NAME%:%BUILD_NUMBER%'
                bat 'kubectl set env deployment/flask-%TARGET% APP_VERSION=%BUILD_NUMBER% APP_COLOR=%TARGET_COLOR%'
                bat 'kubectl rollout status deployment/flask-%TARGET% --timeout=120s'
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    def patch = """{
                        "spec": {
                            "selector": {
                                "app": "blue-green-app",
                                "version": "${env.TARGET}"
                            }
                        }
                    }"""

                    writeFile file: 'service-patch.json', text: patch

                    bat 'kubectl patch service blue-green-service --type merge --patch-file service-patch.json'
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get service blue-green-service'
                bat 'kubectl get deployments'
                bat 'kubectl get pods -l app=blue-green-app'
            }
        }
    }

    post {
        success {
            echo 'Blue-Green deployment completed successfully!'
            echo 'Traffic has been switched to the new environment.'
        }

        failure {
            echo 'Deployment failed. The previous active environment was not intentionally changed.'
            echo 'Check the failed stage before attempting another deployment.'
        }
    }
}
