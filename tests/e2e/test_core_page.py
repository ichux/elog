from secrets import token_hex
from flask_testing import LiveServerTestCase  # type: ignore
from seleniumbase import BaseCase  # type: ignore
import requests  # type: ignore
from dotenv import load_dotenv

load_dotenv()

from elog import elap, db, User  # noqa: E402


class TestCorePage(BaseCase, LiveServerTestCase):
    def create_app(self):
        elap.config['TESTING'] = True
        elap.config['SECRET_KEY'] = token_hex(12)
        elap.config['LIVESERVER_PORT'] = 9000
        elap.config['LIVESERVER_TIMEOUT'] = 10
        return elap

    def setUp(self, masterqa_mode=False):
        super(TestCorePage, self).setUp(BaseCase)
        super(TestCorePage, self).setUp(LiveServerTestCase)
        self.username = token_hex(6)
        self.pwd = token_hex(12)
        self.user = User(username=self.username)
        self.user.set_password(self.pwd)
        db.session.add(self.user)
        db.session.commit()
        self.login()
        self.trigger_error()

    def tearDown(self):
        db.session.query(User).filter(User.username == self.username).delete()
        db.session.commit()

    def login(self):
        self.goto(f"{self.get_server_url()}/auth")
        self.input('input[placeholder="Username"]', self.username)
        self.input('input[placeholder="Password"]', self.pwd)
        self.submit('form')

        self.assert_element('[x-data="elog"]')

    def trigger_error(self):
        """This will trigger a 404 error to have at least one entry in the logs"""
        requests.get(f"{self.get_server_url()}/favicon.ico")

    def test_records_shown(self):
        self.goto(self.get_server_url())
        self.wait(5)
        self.reload()
        self.assert_elements('table')

    def test_record_details(self):
        self.goto(self.get_server_url())
        self.reload()
        self.assert_element('tr.gridjs-tr')
        row = self.get_element('tr.gridjs-tr')
        print(row)
        row.click()
        self.wait(12)
