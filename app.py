from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Python DevOps App Running"

@app.route("/health")
def health():
    cpu = os.popen("top -bn1 | grep 'Cpu(s)'").read()
    return f"CPU Status: {cpu}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
