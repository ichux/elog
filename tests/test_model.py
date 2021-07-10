import unittest

from dotenv import load_dotenv

load_dotenv()

from elog import db  # noqa: E402
from elog.models import compile_query  # noqa: E402
from elog.models.profile import User  # noqa: E402


class ModelFile(unittest.TestCase):
    def setUp(self):
        self.username = "test1"
        self.tables = ["users", "user_accesses"]

    def test_compile_query(self):
        user = User.query.filter_by(username=self.username)
        self.assertIn(self.username, str(compile_query(user)))

    def test_show_all(self):
        for k, v in db.metadata.tables.items():
            self.assertIn(k, self.tables)
