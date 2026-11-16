
import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")
APP_COLOR = os.getenv("APP_COLOR", "Blue")

@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>Blue-Green Deployment</title>
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                padding-top: 100px;
                background: #f4f4f4;
            }}
            .container {{
                background: white;
                padding: 40px;
                margin: auto;
                width: 450px;
                border-radius: 12px;
                box-shadow: 0 0 10px #ccc;
            }}
            h1 {{ color: {APP_COLOR.lower()}; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{APP_COLOR} Environment</h1>
            <h2>Blue-Green Deployment Demo</h2>
            <p>Application Version: {APP_VERSION}</p>
            <p>Deployment Strategy: Blue-Green</p>
            <p>Status: Running Successfully</p>
        </div>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "environment": APP_COLOR
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
