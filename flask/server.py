from flask import Flask
import os

var1 = os.environ['BLA']

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, my name is ' + var1 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)