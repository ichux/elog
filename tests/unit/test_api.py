import collections
import secrets
import unittest
from datetime import datetime

from dotenv import load_dotenv
from webtest import TestApp  # type: ignore
from webtest.app import AppError  # type: ignore

load_dotenv()


from elog import db, elap  # noqa: E402
from elog.models.profile import User, UserAccess  # noqa: E402


class RESTRoutes(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(elap)
        self.api_route = "/api/v1.0/elog"
        self.auth_url = "/auth/?next=%2F"
        self.username = "test1"
        self.password = "T35tW!thiChux"
        self.ip_address = "127.0.0.1"
        self.data_url = "/data?draw=1&start=0&length=20"

    def test_create_user(self):
        """
        Test to create a test user if it doesn't exist
        """
        user = User.query.filter_by(username=self.username).first()

        if not user:
            user = User(username=self.username)

        user.set_password(self.password)
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.username, self.username)
        self.assertTrue(user.verify_password(self.password))

    def test_add_access(self):
        """
        Test to enable user access to the application
        """
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
        """
        Test for login from the frontend
        """
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
        self.assertNotIn(b"errormsg", self.app.get("/").body)

        self.app.get("/auth/logout")
        self.assertEqual(response.status_code, 200)

    def test_404_error(self):
        """
        Test for Error 404 using the first method
        """
        with self.assertRaises(AppError):
            self.app.get("/unknown-route")

    def test_404_error_2(self):
        """
        Test for Error 404 using a second method
        """
        self.app.get(
            "/unknown-route",
            expect_errors=True,
        )

    def test_existence_of_path(self):
        """
        After the generation of Error 404
        This tests for the existence of the data
        """
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

        print(response)

        for each in response.json.get("data"):
            request_path = each.get("requestpath")
            if request_path == "/unknown-route":
                self.assertTrue(request_path)
                break

    def test_details(self):
        """
        Tests the details of a user
        """
        user = User.query.filter_by(username=self.username).first()
        for _ in user.known_access:
            if _.ip_address == self.ip_address:
                self.assertTrue(_.external_app_id)
                self.assertTrue(_.enabled)
                break

    @unittest.skip("essential skip")
    def test_elog_api(self):
        """
        Sends data to the API route
        """
        str_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        ext_app_id = None

        user = User.query.filter_by(username=self.username).first()

        for _ in user.known_access:
            if _.ip_address == self.ip_address:
                ext_app_id = _.external_app_id
                break

        response = self.app.post_json(
            self.api_route,
            {
                "ip": "127.0.0.1",
                "requestpath": "/api/v1.0/elog",
                "httpmethod": "POST",
                "useragent": (
                    "Mozilla/5.0 (Windows NT 5.1; WOW64; rv:39.0) Gecko/20100101"
                    "Firefox/39.0"
                ),
                "userplatform": "Linux",
                "userbrowser": "Mozilla Firefox",
                "userbrowserversion": "39.0",
                "referrer": "None",
                "requestargs": "None",
                "postvalues": "None",
                "errortype": "Error 404",
                "errormsg": "Error 404",
                "when": str_date_time,
                "errortraceback": "errortraceback...",
                "code": 404,
                "date": str_date_time,
            },
            headers={"EXTERNAL-APP-ID": ext_app_id},
        )

        # self.assertEqual(response.request.headers["External-App-Id"], ext_app_id)
        # HTTP_EXTERNAL_APP_ID
        for k, v in response.request.headers.items():
            print(k, v)
