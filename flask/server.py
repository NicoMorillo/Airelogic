from flask import Flask
import os

var1 = os.environ['NAME']

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, my name is ' + var1 

@app.route('/Alice')
def Alice():
    return 'Hello, my name is Alice' 

@app.route('/Bob')
def Bob():
    return 'Hello, my name is Bob'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)