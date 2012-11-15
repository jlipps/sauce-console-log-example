# encoding: utf-8
import unittest
import json
import time
import httplib
import base64

from selenium import webdriver


def setUp():
    with open("auth.json") as fi:
        auth = json.load(fi)
        Selenium2OnSauce.user = auth['user']
        Selenium2OnSauce.key = auth['key']


class Selenium2OnSauce(unittest.TestCase):

    _basic_auth = None

    # set by setUp
    user = None
    key = None

    def setUp(self):
        self._passed = False

        desired_capabilities = webdriver.DesiredCapabilities.CHROME
        desired_capabilities['version'] = ''
        desired_capabilities['platform'] = 'Windows 2003'
        desired_capabilities['name'] = 'Naminator works'

        self.driver = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://{0.user}:{0.key}@ondemand.saucelabs.com:80/wd/hub".format(self)
        )
        self.driver.implicitly_wait(30)
        self.test_id = self.driver.session_id
        print "Test is running at https://saucelabs.com/jobs/%s" % self.test_id

    def _send_passed(self):
        """Tell Sauce Labs whether the test passed."""
        if not self._basic_auth:
            self._basic_auth = "Basic {}".format(
                base64.encodestring("{0.user}:{0.key}".format(self))[:-1])

        body = json.dumps(dict(passed=self._passed))
        url = "/rest/v1/{0.user}/jobs/{0.test_id}".format(self)
        headers = {'Authorization': self._basic_auth}

        connection = httplib.HTTPSConnection("saucelabs.com")
        connection.request(method='PUT', url=url, body=body, headers=headers)
        return connection.getresponse().status == 200

    def test_naminator(self):
        self.driver.get('http://localhost:5050/')
        self.assertIn("naminator", self.driver.title.lower())

        # enter the names
        self.driver.find_element_by_id("names").click()
        self.driver.find_element_by_id("names").clear()
        self.driver.find_element_by_id("names").send_keys("sauce jquery selenium")

        # namiratorize!
        self.driver.find_element_by_id("doItNau").click()

        # get/wait for namiratorizations
        naminatorized = self.driver.find_element_by_tag_name("html").text
        for _ in xrange(20):
            if not "Naminatorized stuff" in naminatorized:
                break

            time.sleep(0.25)
            naminatorized = self.driver.find_element_by_tag_name("html").text
        else:
            assert False, "-ators never showed up"

        self.assertIn("saucinator", naminatorized)
        self.assertIn("jquerynator", naminatorized)
        self.assertIn("seleniuminator", naminatorized)

        self._passed = True

    def tearDown(self):
        self._send_passed()  # mark the test pass/fail on sauce
        self.driver.quit()


if __name__ == '__main__':
    setUp()
    unittest.main()
