# encoding: utf-8
import json
import unittest

from selenium import webdriver


class Selenium2OnSauce(unittest.TestCase):

    user = None
    key = None

    def setUp(self):
        desired_capabilities = webdriver.DesiredCapabilities.CHROME
        desired_capabilities['version'] = ''
        desired_capabilities['platform'] = 'Windows 2003'
        desired_capabilities['name'] = 'Naminator works'

        self.driver = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://{0.user}:{0.key}@ondemand.saucelabs.com:80/wd/hub".format(self)
        )
        self.driver.implicitly_wait(30)

    def test_sauce(self):
        self.driver.get('http://r00.local:5050/')
        self.assertIn("naminator", self.driver.title.lower())

        self.driver.find_element_by_id("names").click()
        self.driver.find_element_by_id("names").clear()
        self.driver.find_element_by_id("names").send_keys("sauce jquery selenium")
        self.driver.find_element_by_id("doItNau").click()

        naminatorized = self.driver.find_element_by_tag_name("html").text
        self.assertIn("saucinator", naminatorized)
        self.assertIn("jquerynator", naminatorized)
        self.assertIn("seleniuminator", naminatorized)

    def tearDown(self):
        print "Test page is https://saucelabs.com/jobs/%s" % self.driver.session_id
        self.driver.quit()


if __name__ == '__main__':
    with open("auth.json") as fi:
        auth = json.load(fi)
        Selenium2OnSauce.user = auth['user']
        Selenium2OnSauce.key = auth['key']

    unittest.main()
