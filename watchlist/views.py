from watchlist import app, db
from watchlist.models import User, Movie, Comment
from flask import url_for, render_template, redirect, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from markupsafe import escape
from datetime import datetime


@app.context_processor
def inject_user():
    from watchlist.models import User

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Invalid Input")
            return redirect(url_for("login"))

        user = User.query.first()
        if username == username and user.validate_password(password):
            login_user(user)
            flash("Login Success")
            return redirect(url_for("index"))

        flash("Invalid username or password")
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Goodbye")
    return redirect(url_for("index"))


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = request.form["name"]
        if not name or len(name) > 20:
            flash("Invalid Input")
            return redirect(url_for("settings"))
        current_user.name = name
        db.session.commit()
        flash("Setting Updated")
        return redirect(url_for("index"))
    return render_template("settings.html")


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


@app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required
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
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item Deleted.")
    return redirect(url_for("index"))


@app.route("/comments", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        time = datetime.now()
        if not name or not message or len(name) > 60 or len(message) > 2000:
            flash("Invalid Input.")
            return redirect(url_for("comment"))
        one_comment = Comment(name=name, message=message, time=time)
        db.session.add(one_comment)
        db.session.commit()
        flash('Comment Created!')
        return redirect(url_for('comment'))
    comments = Comment.query.all()
    return render_template("comments.html", comments=comments)
