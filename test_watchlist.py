import unittest
from app import app, db, Movie, User, forge, initdb, admin


class WatchlistTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        db.create_all()
        user = User(name="Test", username="test")
        user.set_password("abc")
        movie = Movie(title="Test Movie", year="2023")
        db.session.add_all([user, movie])
        db.session.commit()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config["TESTING"])

    def test_404_page(self):
        response = self.client.get("/nothing")
        data = response.get_data(as_text=True)
        self.assertIn("Page Not Found - 404", data)
        self.assertIn("Go Back", data)
        self.assertEqual(response.status_code, 404)

    def test_index_page(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("Test's Watchlist", data)
        self.assertIn("Test Movie", data)
        self.assertEqual(response.status_code, 200)

    # 辅助方法，用于登入用户
    def login(self):
        self.client.post(
            "/login", data=dict(username="test", password="abc"), follow_redirects=True
        )

    def test_create_item(self):
        self.login()
        # 测试创建条目操作
        response = self.client.post(
            "/", data=dict(title="New Movie", year="2023"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Item created.", data)
        self.assertIn("New Movie", data)
        # 测试创建条目条件
        # 电影标题为空
        response = self.client.post(
            "/", data=dict(title="", year="2023"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item created.", data)
        self.assertIn("Invalid Input.", data)
        # 电影年份为空
        response = self.client.post(
            "/", data=dict(title="New Movie", year=""), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item created.", data)
        self.assertIn("Invalid Input.", data)

    def test_update_item(self):
        self.login()

        # 测试更新页面
        response = self.client.get("/movie/edit/1")
        data = response.get_data(as_text=True)
        self.assertIn("Test Movie", data)
        self.assertIn("2023", data)

        # 测试更新条目操作
        response = self.client.post(
            "/movie/edit/1",
            data=dict(title="New Movie Edited", year="2019"),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("Item Updated.", data)
        self.assertIn("New Movie Edited", data)

        # 测试更新条目操作，但电影标题为空
        response = self.client.post(
            "/movie/edit/1", data=dict(title="", year="2019"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item Updated.", data)
        self.assertIn("Invalid Input.", data)

        # 测试更新条目操作，但电影年份为空
        response = self.client.post(
            "/movie/edit/1",
            data=dict(title="New Movie Edited Again", year=""),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item Updated.", data)
        self.assertNotIn("New Movie Edited Again", data)
        self.assertIn("Invalid Input.", data)

    def test_delete_item(self):
        self.login()
        response = self.client.post("/movie/delete/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Item Deleted.", data)
        self.assertNotIn("New Movie Edited", data)

    def test_login_protect(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertNotIn("logout", data)
        self.assertNotIn("Settings", data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn("delete", data)
        self.assertNotIn("Edit", data)

    def test_login(self):
        response = self.client.post(
            "/login", data=dict(username="test", password="abc"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Login Success", data)
        self.assertIn("logout", data)
        self.assertIn("Settings", data)
        self.assertIn("delete", data)
        self.assertIn("Edit", data)
        self.assertIn('<form method="post">', data)

        # 测试使用错误的密码登录
        response = self.client.post(
            "/login", data=dict(username="test", password="789"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Invalid username or password", data)
        self.assertNotIn("Login Success", data)

        # 测试使用错误的用户名登录
        response = self.client.post(
            "/login",
            data=dict(username="wrongname", password="123"),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("Invalid username or password", data)
        self.assertNotIn("Login Success", data)

        # 测试使用空用户名登录
        response = self.client.post(
            "/login", data=dict(username="", password="123"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Invalid Input", data)
        self.assertNotIn("Login Success", data)

        # 测试使用空密码登录
        response = self.client.post(
            "/login", data=dict(username="test", password=""), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Invalid Input", data)
        self.assertNotIn("Login Success", data)

    def test_logout(self):
        self.login()
        # 测试设置页面
        response = self.client.get("/logout", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Goodbye", data)
        self.assertNotIn("logout", data)
        self.assertNotIn("Settings", data)
        self.assertNotIn("delete", data)
        self.assertNotIn("Edit", data)
        self.assertNotIn('<form method="post">', data)

    def test_settings(self):
        self.login()
        # 测试设置页面
        response = self.client.get("/settings")
        data = response.get_data(as_text=True)
        self.assertIn("Settings", data)
        self.assertIn("Your name", data)

        # 测试更新设置
        response = self.client.post(
            "/settings", data=dict(name="Yzm22"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Setting Updated", data)
        self.assertIn("Yzm22", data)

        # 名称为空
        response = self.client.post(
            "/settings", data=dict(name=""), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Setting Updated", data)
        self.assertIn("Invalid Input", data)

    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn("Done.", result.output)
        self.assertNotEqual(Movie.query.count(), 0)

    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn("Initialized database.", result.output)

    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(
            args=["admin", "--username", "yzm", "--password", "abc"]
        )
        self.assertIn("Creating User...", result.output)
        self.assertIn("Done.", result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, "yzm")
        self.assertTrue(User.query.first().validate_password("abc"))

    def test_admin_command_update(self):
        result = self.runner.invoke(
            args=["admin", "--username", "yzm", "--password", "123"]
        )
        self.assertIn("Updating user...", result.output)
        self.assertIn("Done.", result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, "yzm")
        self.assertTrue(User.query.first().validate_password("123"))


if __name__ == "__main__":
    unittest.main()
