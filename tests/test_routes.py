import unittest

from dotenv import load_dotenv
from webtest import TestApp  # type: ignore

load_dotenv()

from elog import elap  # noqa: E402


class NonRESTRoutes(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(elap)
        self.auth_url = "/auth/?next=%2F"

    def test_index(self):
        response = self.app.get("/")

        self.assertEqual(response.content_type, "text/html")
        self.assertEqual(response.status, "302 FOUND")
        self.assertIn(b"/auth/?next=%2F", response.body)

        response = self.app.get("/")
        self.assertNotIn(b"errormsg", response.body)
