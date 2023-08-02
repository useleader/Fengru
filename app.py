# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# @file         :app.py
# @description  :
# @time         :2023/07/24 21:40:21
# @author       :Yan ZhiMin
# @version      :1.0
# """

# import os
# import sys
# import click
# from flask import Flask, url_for, render_template, request, flash, redirect
# from markupsafe import escape
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import (
#     LoginManager,
#     UserMixin,
#     login_user,
#     login_required,
#     logout_user,
#     current_user,
# )

# WIN = sys.platform.startswith("win")
# prefix = ""
# if WIN:
#     prefix = "sqlite:///"
# else:
#     prefix = "sqlite:////"

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path, "data.db")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # 关闭对模型修改的监控
# app.config["SECRET_KEY"] = "yzmyyds"  # 正常应为随机串，且不应以明文写在代码中

# db = SQLAlchemy(app)  # 在扩展类实例化前加载配置
# login_manager = LoginManager(app)


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)  # key
#     name = db.Column(db.String(20))  # users' name
#     username = db.Column(db.String(20))
#     password_hash = db.Column(db.String(128))

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def validate_password(self, password):
#         return check_password_hash(self.password_hash, password)


# class Movie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(60))
#     year = db.Column(db.String(4))


# @login_manager.user_loader
# def load_user(user_id):
#     user = User.query.get(int(user_id))
#     return user


# @app.cli.command()  # 注册为命令，可以传入name参数来自定义命令
# @click.option("--drop", is_flag=True, help="Create after drop.")  # 设置选项
# def initdb(drop):
#     """Initialize the database."""
#     if drop:
#         db.drop_all()
#     db.create_all()
#     click.echo("Initialized database.")


# @app.cli.command()
# @click.option("--yzm", is_flag=True, help="say hello to everyone.")
# def say_hello(yzm):
#     """we should be polite, so say hello to everyone!"""
#     if yzm:
#         click.echo("Hello, everyone! My name is Yan Zhimin.")
#     else:
#         click.echo("Hello~~")


# @app.cli.command()
# def forge():
#     """Generate fake data."""
#     db.create_all()

#     # 全局的两个变量移动到这个函数内
#     name = "Grey Li"
#     movies = [
#         {"title": "My Neighbor Totoro", "year": "1988"},
#         {"title": "Dead Poets Society", "year": "1989"},
#         {"title": "A Perfect World", "year": "1993"},
#         {"title": "Leon", "year": "1994"},
#         {"title": "Mahjong", "year": "1996"},
#         {"title": "Swallowtail Butterfly", "year": "1996"},
#         {"title": "King of Comedy", "year": "1999"},
#         {"title": "Devils on the Doorstep", "year": "1999"},
#         {"title": "WALL-E", "year": "2008"},
#         {"title": "The Pork of Music", "year": "2012"},
#     ]

#     user = User(name=name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movie(title=m["title"], year=m["year"])
#         db.session.add(movie)

#     db.session.commit()
#     click.echo("Done.")


# @app.cli.command()
# @click.option("--username", prompt=True, help="The username to login.")
# @click.option(
#     "--password",
#     prompt=True,
#     hide_input=False,
#     confirmation_prompt=True,
#     help="The password used to login.",
# )
# def admin(username, password):
#     """Create user"""
#     db.create_all()
#     user = User.query.first()  # 这个实现的方法就一个管理员
#     if user is not None:
#         click.echo("Updating user...")
#         user.username = username
#         user.set_password(password)
#     else:
#         click.echo("Creating User...")
#         user = User(username=username, name="Admin")
#         user.set_password(password=password)
#         db.session.add(user)
#     db.session.commit()
#     click.echo("Done.")


# @app.context_processor
# def inject_user():
#     user = User.query.first()
#     return dict(user=user)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         title = request.form.get("title")
#         year = request.form.get("year")
#         if not title or not year or len(year) > 4 or len(title) > 60:
#             flash("Invalid Input.")
#             return redirect(url_for("index"))
#         movie = Movie(title=title, year=year)
#         db.session.add(movie)
#         db.session.commit()
#         flash("Item created.")
#         return redirect(url_for("index"))
#     movies = Movie.query.all()
#     return render_template("index.html", movies=movies)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         if not username or not password:
#             flash("Invalid Input")
#             return redirect(url_for("login"))

#         user = User.query.first()
#         if username == username and user.validate_password(password):
#             login_user(user)
#             flash("Login Success")
#             return redirect(url_for("index"))

#         flash("Invalid username or password")
#         return redirect(url_for("login"))
#     return render_template("login.html")


# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("Goodbye")
#     return redirect(url_for("index"))


# @app.route('/settings', methods=['GET', 'POST'])
# @login_required
# def settings():
#     if request.method == 'POST':
#         name = request.form['name']
#         if not name or len(name) > 20:
#             flash('Invalid Input')
#             return redirect(url_for('settings'))
#         current_user.name = name
#         db.session.commit()
#         flash('Setting Updated')
#         return redirect(url_for('index'))
#     return render_template('settings.html')

# @app.route("/user/<name>")
# def user_page(name):
#     return f"Wlcome to {escape(name)}"


# @app.route("/test")
# def test_url_for():
#     print(url_for("hello_world"))
#     print(url_for("user_page", name="yzm"))
#     print(url_for("user_page", name="Alice"))
#     print(url_for("test_url_for"))
#     print(url_for("test_url_for", num=2))
#     print(url_for("static", filename="favicon.png"))
#     return "Test Page"


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("404.html"), 404


# @app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
# @login_required
# def edit(movie_id):
#     movie = Movie.query.get_or_404(movie_id)
#     if request.method == "POST":
#         title = request.form["title"]
#         year = request.form["year"]
#         if not title or not year or len(year) != 4 or len(title) > 60:
#             flash("Invalid Input.")
#             return redirect(url_for("edit", movie_id=movie_id))
#         movie.title = title
#         movie.year = year
#         db.session.commit()  # 更新
#         flash("Item Updated.")
#         return redirect(url_for("index"))
#     return render_template("edit.html", movie=movie)


# @app.route("/movie/delete/<int:movie_id>", methods=["POST"])  # 限定只接受 POST 请求
# @login_required
# def delete(movie_id):
#     movie = Movie.query.get_or_404(movie_id)
#     db.session.delete(movie)
#     db.session.commit()
#     flash("Item Deleted.")
#     return redirect(url_for("index"))
