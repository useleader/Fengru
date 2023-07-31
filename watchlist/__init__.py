import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yzmyyds'
prefix = 'sqlite:///' if sys.platform.startswith("win") else 'sqlite:////'
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(os.path.dirname(app.root_path), "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)
login_manager = LoginManager(app=app)

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import views, errors, commands
