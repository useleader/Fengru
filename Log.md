# 7.24学习记录

- 程序托管回顾

```bash
git config --global --list # 查看自己的用户名和邮箱

git add . # add all files to buffer

git commit -m "update Message"

git push # update to gitee

git branch # show all local branches

git branch -r # show all remote branches

git branch [branch-name] # new a branch, but remain current branch

git checkout -b [branch] # new a branch, and switch to this branche

git checkout "branch-name" # switch to this branch

git merge [branch] # 合并制定分支到当前分支

git branch -d [branch-name] # delete the branch

git push origin --delete [branch-name] # delete remote branch

git branch -dr [remote/branch] # delete remote branch
```

## 参考资料

1. [Git使用详解](https://blog.csdn.net/qq_57581439/article/details/124237905)
2. [Markdown语法](https://blog.csdn.net/github_38336924/article/details/82183088)

# 7.25学习记录

- 昨天的补充
  - 在运行虚拟环境前需要先确保安装了virtual
- 环境变量管理
    ```bash
    export FLASK_DEBUG=1
    flask run
    # 或者可以使用自动导入环境变量的python-dotenv
    # 高版本Flask可以
    flask run --dubug
    ```
    `.env`文件用来存储敏感数据，不提交进Git仓库

    `.flaskenv`文件将环境设为`FLASK_DEBUG`设为1,以便开启调试模式

    用户输入的数据可能包含恶意代码，不能直接作为响应返回，需要使用`MarkupSafe`提供的`escape()`对变量进行转义处理
- 数据库
  
   使用`SQLALchemy`--Python数据库工具，通过定义Python类来表示数据库里的一张表（类属性表示表中的字段/列），通过对类操作来代替写SQL语句，这个类称为模型类，类中属性称为字段。

   ```bash
    pip install flask-sqlalchemy==2.5.1 sqlalchemy==1.4.47
    #  Flask-SQLAlchemy 3.x / SQLAlchemy 2.x 版本有一些大的变化，这里分别固定安装 2.5.1 和 1.4.47 版本。
   ```

   为了设置Flask/扩展/程序本身的一些行为，需要设置和定义一些配置变量。Flask提供了一个统一的接口来写入和获取这些配置变量: `Flask.config`字典。配置变量的名称必须是使用大写，写入配置的语句一般会放到扩展类实例化语句之前。
   ```python
    import os
    # SQLALCHEMY_DATABASE_URI变量来告诉SQLAlchemy数据库连接地址
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
   ```
   在Windows中是3个`/`，linux或Mac中是4个`/`
   如果出现了`Instance of 'SQLALchemy' has no 'xxx' member`的情况，是由于`pylint`的事情，改为`flake8`，要禁用`pylint`才行，但我感觉是我没设置好的问题（在settings.json中设置）
   如果出现了长度报错的问题，在`python-Linting`中添加相关的限定长度。
  ```bash
  (env) $ flask shell # 创建db文件
  >>> from app import db
  >>> db.create_all()
  ```
  - 创建

  ```python
  >>> from app import User, Movie  # 导入模型类
  >>> user = User(name='Grey Li')  # 创建一个 User 记录
  >>> m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
  >>> m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
  >>> db.session.add(user)  # 把新创建的记录添加到数据库会话
  >>> db.session.add(m1)
  >>> db.session.add(m2)
  >>> db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
  ```

  当实例化模型类时，如果没有传入主键，SQLAlchemy会自动处理该字段

  - 读取

    `<模型类>.query.<过滤方法(可选)>.<查询方法>`

    具体的过滤方法和常用的查询方法都在参考资料2中指出。
  
  - 更新

    ```python
    >>> movie = Movie.query.get(2)
    >>> movie.title = 'WALL-E'  # 直接对实例属性赋予新的值即可
    >>> movie.year = '2008'
    >>> db.session.commit()  # 注意仍然需要调用这一行来提交改动
    ```
  
  - 删除

  ```python
  >>> movie = Movie.query.get(1)
  >>> db.session.delete(movie)  # 使用 db.session.delete() 方法删除记录，传入模型实例
  >>> db.session.commit()  # 提交改动
  ```  

- 在程序里操作数据库

  ```python
  @app.cli.command()
  @click.option('--xxx', is_flag=True, help='yyy')
  def command_name(arg):
    """Description"""
    if arg:
      return 
    else:
      return 
  ```
- 模板信息
  - vscode中 “File”—“Preferences”—“User Snippets”选择python
  ```json 
    {
    "HEADER": {
        "prefix": "header",
        "body": [
        "#!/usr/bin/env python",
        "# -*- encoding: utf-8 -*-",
        "'''",
        "@文件    :$TM_FILENAME",
        "@说明    :",
        "@时间    :$CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE:$CURRENT_SECOND",
        "@作者    :张三",
        "@版本    :1.0",
        "'''",
        "",
        "$0"
        ],
    }
    }
  ```
    之后在头部敲入header即可自动弹出上面的注释。
## 参考资料

1. [Hello,Flask!](https://tutorial.helloflask.com/hello/)
2. [数据库](https://tutorial.helloflask.com/database/)
3. [添加Python模板信息](www.yisu.com/zixun/155844.html)
4. [SQLAlchemy报错解决方案](https://blog.csdn.net/stone0823/article/details/90488029)