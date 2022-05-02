from secrets import token_hex
from flask_testing import LiveServerTestCase  # type: ignore
from seleniumbase import BaseCase  # type: ignore
from dotenv import load_dotenv

load_dotenv()

from elog import elap, db, User  # noqa: E402


class TestAuthPage(BaseCase, LiveServerTestCase):
    def create_app(self):
        elap.config['TESTING'] = True
        elap.config['SECRET_KEY'] = token_hex(12)
        elap.config['LIVESERVER_PORT'] = 9000
        elap.config['LIVESERVER_TIMEOUT'] = 10
        return elap

    def setUp(self, masterqa_mode=False):
        super(TestAuthPage, self).setUp(BaseCase)
        super(TestAuthPage, self).setUp(LiveServerTestCase)
        self.username = token_hex(6)
        self.pwd = token_hex(12)
        self.user = User(username=self.username)
        self.user.set_password(self.pwd)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.query(User).filter(User.username == self.username).delete()
        db.session.commit()

    def test_got_redirected_when_not_auth(self):
        self.goto(self.get_server_url())
        self.assertIn(f"{self.get_server_url()}/auth", self.get_current_url())

    def test_valid_login(self):
        self.goto(f"{self.get_server_url()}/auth")
        self.input('input[placeholder="Username"]', self.username)
        self.input('input[placeholder="Password"]', self.pwd)
        self.submit('form')

        self.assert_element('[x-data="elog"]')

    def test_logout(self):
        self.goto(f"{self.get_server_url()}/auth")
        self.input('input[placeholder="Username"]', self.username)
        self.input('input[placeholder="Password"]', self.pwd)
        self.submit('form')

        self.click('div#logout-dropdown')
        self.click('div#logout-dropdown a')

        self.assertIn(f"{self.get_server_url()}/auth", self.get_current_url())
