import collections
import secrets
import unittest

from dotenv import load_dotenv
from webtest import TestApp  # type: ignore
from webtest.app import AppError  # type: ignore

load_dotenv()


from elog import db, elap  # noqa: E402
from elog.models.profile import User, UserAccess  # noqa: E402


class RESTRoutes(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(elap)
        self.auth_url = "/auth/?next=%2F"
        self.username = "test1"
        self.password = "T35tW!thiChux"
        self.ip_address = "127.0.0.1"
        self.data_url = "/data?draw=1&start=0&length=20"

    def test_create_user(self):
        user = User.query.filter_by(username=self.username).first()

        if not user:
            user = User(username=self.username)

        user.set_password(self.password)
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.username, self.username)
        self.assertTrue(user.verify_password(self.password))

    def test_add_access(self):
        user = User.query.filter_by(username=self.username).first()

        if user:
            user_access = (
                UserAccess.query.filter_by(users_id=user.id)
                .filter_by(ip_address=self.ip_address)
                .first()
            )
            if not user_access:
                user_access = UserAccess(users_id=user.id, ip_address=self.ip_address)

            user_access.external_app_id = secrets.randbits(32)
            db.session.add(user_access)
            db.session.commit()

            self.assertTrue(user_access.external_app_id)
            self.assertEqual(user_access.ip_address, self.ip_address)

    def test_login(self):
        response = self.app.get(self.auth_url)
        self.assertEqual(response.status_code, 200)

        data = collections.OrderedDict(
            [
                ("username", self.username),
                ("password", self.password),
                ("csrf_token", response.forms[1]["csrf_token"].value),
            ]
        )

        self.app.post(self.auth_url, data)
        self.assertIn(b"errormsg", self.app.get("/").body)

        self.app.get("/auth/logout")
        self.assertEqual(response.status_code, 200)

    def test_404_error(self):

        with self.assertRaises(AppError):
            self.app.get("/unknown-route")

    def test_404_error_2(self):
        self.app.get(
            "/unknown-route",
            expect_errors=True,
        )

    def test_existence_of_path(self):
        response = self.app.get(self.auth_url)
        self.assertEqual(response.status_code, 200)

        data = collections.OrderedDict(
            [
                ("username", self.username),
                ("password", self.password),
                ("csrf_token", response.forms[1]["csrf_token"].value),
            ]
        )

        self.app.post(self.auth_url, data)

        response = self.app.get(
            self.data_url,
            xhr=True,
        )

        for each in response.json.get("data"):
            request_path = each.get("requestpath")
            if request_path == "/unknown-route":
                self.assertTrue(request_path)
                break
