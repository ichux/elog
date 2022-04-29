from secrets import token_hex

from flask_testing import LiveServerTestCase
from seleniumbase import BaseCase

from elog import elap, db  # noqa: E402
from flask_migrate import Migrate


class TestAuthPage(BaseCase, LiveServerTestCase):
    def create_app(self):
        elap.config['TESTING'] = True
        elap.config['SECRET_KEY'] = token_hex(12)
        elap.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        elap.config['LIVESERVER_PORT'] = 9000
        elap.config['LIVESERVER_TIMEOUT'] = 10
        db.init_app(elap)
        Migrate(elap, db)
        return elap

    def test_got_redirected_when_not_auth(self):
        self.goto(self.get_server_url())
        self.assertIn(f"{self.get_server_url()}/auth", self.get_current_url())

    def test_(self):
        self.goto(f"{self.get_server_url()}/auth")
        self.input('input[placeholder="Username"]', 'hans')
        self.input('input[placeholder="Password"]', 'hans')
        self.submit('form')
