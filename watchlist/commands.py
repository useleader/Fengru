import click
from watchlist import app, db
from watchlist.models import User, Movie


@app.context_processor
def inject_user():
    from watchlist.models import User

    user = User.query.first()
    return dict(user=user)


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


@app.cli.command()
@click.option("--username", prompt=True, help="The username to login.")
@click.option(
    "--password",
    prompt=True,
    hide_input=False,
    confirmation_prompt=True,
    help="The password used to login.",
)
def admin(username, password):
    """Create user"""
    db.create_all()
    user = User.query.first()  # 这个实现的方法就一个管理员
    if user is not None:
        click.echo("Updating user...")
        user.username = username
        user.set_password(password)
    else:
        click.echo("Creating User...")
        user = User(username=username, name="Admin")
        user.set_password(password=password)
        db.session.add(user)
    db.session.commit()
    click.echo("Done.")
