from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/python')
def hello_python():
	return 'hello python'

@app.route('/python/flask')
def hello_flask():
	return 'hello flask'
