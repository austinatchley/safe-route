import os

from flask import Flask
app = Flask(__name__, instance_relative_config=True)

@app.route('/')
def home():
    return "home"
