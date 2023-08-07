import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# 配置app相关属性，密钥，数据库

prefix = "sqlite:///" if sys.platform.startswith("win") else "sqlite:////"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "yzmyyds")
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(
    os.path.dirname(app.root_path, os.getenv("DATABASE_FILE", "data.db"))
)

# 关闭对模型修改的监控

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# 数据库部分

db = SQLAlchemy(app)
login_manager = LoginManager(app=app)

@login_manager.user_loader
def load_user(user_id):
    from chatlist.models import  
