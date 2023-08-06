from qrunner.utils.log import logger
from qrunner.core.web.driver import relaunch
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# 安卓webview元素
class Element:
    def __init__(self, h5_driver, xpath=None, css=None, index=0):
        self.driver = h5_driver
        self.d = self.driver.d
        self.locator = None
        self.index = index
        if xpath:
            self.locator = (By.XPATH, xpath)
        if css:
            self.locator = (By.CSS_SELECTOR, css)

    @relaunch
    def wait(self, timeout=10):
        wait = WebDriverWait(self.d, timeout=timeout)
        try:
            wait.until(EC.presence_of_element_located(self.locator))
            return True
        except:
            self.driver.screenshot(f'元素定位失败: {self.locator}')
            # logger.info(f'页面内容: \n{self.driver.get_ui_tree()}')
            raise AssertionError(f'元素定位失败: {self.locator}')

    @relaunch
    def get_element(self):
        if self.wait():
            element = self.d.find_elements(self.locator[0], self.locator[1])[self.index]
            return element

    @relaunch
    def click(self):
        logger.info(f'点击元素: {self.locator}')
        self.get_element().click()

    @relaunch
    def get_text(self):
        logger.info(f'获取元素文案: {self.locator}')
        return self.get_element().text



