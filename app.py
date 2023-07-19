from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>hello world</h1><img src="http://127.0.0.1:5000/src/image/Bob.jpeg">'

@app.route('/python')
def hello_python():
	return 'hello python'

@app.route('/python/flask')
def hello_flask():
	return 'hello flask'

@app.route('/user/<name>')
def user_page(name):
	return f'Wlcome to {escape(name)}'

@app.route('/test')
def test_url_for():
	print(url_for('hello_world'))
	print(url_for('user_page', name='yzm'))
	print(url_for('user_page', name='Alice'))
	print(url_for('test_url_for'))
	print(url_for('test_url_for', num=2))
	return 'Test Page'



name = 'Yan Zhimin'
movies = [
	{'title': '1', 'year': '1988'},
	{'title': '2', 'year': '1989'},
	{'title': '3', 'year': '1993'},
	{'title': '4', 'year': '1982'},
	{'title': '5', 'year': '1989'}
]

@app.route('/index')
def index():
	return render_template('index.html', name=name, movies=movies)
