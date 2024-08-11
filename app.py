from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    print("Hello World")
    return "Hello World"

@app.route("/{name}")
def hello(name):
    return f"Hi {name}"