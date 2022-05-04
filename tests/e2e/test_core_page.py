from secrets import token_hex

import pytest
import requests  # type: ignore
from dotenv import load_dotenv
from flask_testing import LiveServerTestCase  # type: ignore
from selenium.common.exceptions import StaleElementReferenceException
from seleniumbase import BaseCase  # type: ignore

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
        self.reload()
        self.assert_elements('table', 'tr.gridjs-tr', 'td.gridjs-td')

    def test_record_details(self):
        self.goto(self.get_server_url())
        self.reload()
        columns = self.find_elements('td')
        columns[3].click()  # 14 fields with checkboxes first so the choice has to take them into account
        records = [r.text for r in self.find_elements('.info-box__content')]
        columns[17].click()
        records2 = [r.text for r in self.find_elements('.info-box__content')]

        self.assert_elements('aside#record_details', 'aside#record_details .info-box',
                             'aside#record_details .info-box pre code')
        assert records != records2

    def test_action_select_all(self):
        self.goto(self.get_server_url())
        self.reload()
        self.assert_element('#actions .dropdown button')
        self.click('#actions .dropdown button')
        self.click('#select-all')
        checkboxes = self.find_elements('input[type="checkbox"]')
        assert [c.is_selected() for c in checkboxes] == [True for _ in range(len(checkboxes))]

    def test_action_unselect_all(self):
        self.test_action_select_all()  # Because we need to check elements before
        self.click('#actions .dropdown button')
        self.click('#unselect-all')
        checkboxes = self.find_elements('input[type="checkbox"]')
        assert [c.is_selected() for c in checkboxes] == [False for _ in range(len(checkboxes))]

    def test_toggle_action(self):
        self.goto(self.get_server_url())
        self.reload()
        checkboxes = self.find_elements('input[type="checkbox"]')
        checkboxes[0].click()
        assert ([checkboxes[0].is_selected()], [c.is_selected() for c in checkboxes[1:]]) == (
            [True], [False for _ in range(len(checkboxes) - 1)])
        self.click('#actions .dropdown button')
        self.click('#toggle-selection')
        assert ([checkboxes[0].is_selected()], [c.is_selected() for c in checkboxes[1:]]) == (
            [False], [True for _ in range(len(checkboxes) - 1)])

    @pytest.mark.skip(reason="Have to deal with permission issues in navigator")
    def test_copy_as_csv_action(self):
        self.goto(self.get_server_url())
        self.reload()
        checkbox = self.find_elements('input[type="checkbox"]')[0]
        checkbox.click()
        self.click('#actions .dropdown button')
        self.click('#copy-as-csv')
        self.assert_element('.success-popup')

        # This attempt to access the nav clipboard from Javascript
        # to here. It's async and as there no args, arguments[0] represents
        # the callback created by Selenium for us.
        # See
        # https://stackoverflow.com/questions/28057338/understanding-execute-async-script-in-selenium#comment93818104_28066902
        clipboard_content = self.execute_async_script(
            'let c = await navigator.clipboard.readText(); arguments[0](c)')
        print(clipboard_content)
        self.wait(5)

    def test_delete_action(self):
        self.goto(self.get_server_url())
        self.reload()
        checkbox = self.find_element('input[type="checkbox"]')
        checkbox.click()
        self.click('#actions .dropdown button')
        self.click('#delete')
        with pytest.raises(StaleElementReferenceException):
            checkbox.click()
