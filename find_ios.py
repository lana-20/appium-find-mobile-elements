from os import path
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp.app.zip')
APPIUM = 'http://localhost:4723'
CAPS = {
    'platformName': 'iOS',
    'platformVersion': '16.2',
    'deviceName': 'iPhone 14 Pro',
    'automationName': 'XCUITest',
    'app': APP,
}

driver = webdriver.Remote(APPIUM, CAPS)
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Login Screen')))
    driver.find_element(MobileBy.CLASS_NAME, 'XCUIElementTypeStaticText')
    driver.find_element(MobileBy.XPATH, '//XCUIElementTypeOther[@label="Webview Demo"]')
finally:
    driver.quit()
