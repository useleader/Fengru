#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file         :app.py
@description  :
@time         :2023/07/24 21:40:21
@author       :Yan ZhiMin
@version      :1.0
"""

import os
import sys
import click
from flask import Flask, url_for, render_template, request, flash, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith("win")
prefix = ""
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # 关闭对模型修改的监控
app.config["SECRET_KEY"] = "yzmyyds"  # 正常应为随机串，且不应以明文写在代码中

db = SQLAlchemy(app)  # 在扩展类实例化前加载配置


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # key
    name = db.Column(db.String(20))  # users' name


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route("/user/<name>")
def user_page(name):
    return f"Wlcome to {escape(name)}"


@app.route("/test")
def test_url_for():
    print(url_for("hello_world"))
    print(url_for("user_page", name="yzm"))
    print(url_for("user_page", name="Alice"))
    print(url_for("test_url_for"))
    print(url_for("test_url_for", num=2))
    print(url_for("static", filename="favicon.png"))
    return "Test Page"


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("Invalid Input.")
            return redirect(url_for("index"))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Item created.")
        return redirect(url_for("index"))
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


@app.cli.command()  # 注册为命令，可以传入name参数来自定义命令
@click.option("--drop", is_flag=True, help="Create after drop.")  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


@app.cli.command()
@click.option("--yzm", is_flag=True, help="say hello to everyone.")
def say_hello(yzm):
    """we should be polite, so say hello to everyone!"""
    if yzm:
        click.echo("Hello, everyone! My name is Yan Zhimin.")
    else:
        click.echo("Hello~~")


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = "Grey Li"
    movies = [
        {"title": "My Neighbor Totoro", "year": "1988"},
        {"title": "Dead Poets Society", "year": "1989"},
        {"title": "A Perfect World", "year": "1993"},
        {"title": "Leon", "year": "1994"},
        {"title": "Mahjong", "year": "1996"},
        {"title": "Swallowtail Butterfly", "year": "1996"},
        {"title": "King of Comedy", "year": "1999"},
        {"title": "Devils on the Doorstep", "year": "1999"},
        {"title": "WALL-E", "year": "2008"},
        {"title": "The Pork of Music", "year": "2012"},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m["title"], year=m["year"])
        db.session.add(movie)

    db.session.commit()
    click.echo("Done.")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("Invalid Input.")
            return redirect(url_for("edit", movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()  # 更新
        flash("Item Updated.")
        return redirect(url_for("index"))
    return render_template("edit.html", movie=movie)


@app.route("/movie/delete/<int:movie_id>", methods=["POST"])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item Deleted.")
    return redirect(url_for("index"))
