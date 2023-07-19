from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>hello world</h1><img src="https://github.com/useleader/Fengru/blob/main/src/image/Bob.jpeg'

@app.route('/python')
def hello_python():
	return 'hello python'

@app.route('/python/flask')
def hello_flask():
	return 'hello flask'
