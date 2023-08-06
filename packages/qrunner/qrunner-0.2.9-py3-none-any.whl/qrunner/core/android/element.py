import time
from qrunner.utils.log import logger
from qrunner.core.android.driver import Driver


# 初始化driver
driver = Driver()
d = driver.d


# 安卓原生元素
class Element:
    def __init__(self, *args, **kwargs):
        self.element_loc = kwargs
        self.xpath = kwargs.get('xpath', '')
        self.index = kwargs.pop('index', '')
        self.element = d.xpath(self.xpath) if self.xpath else d(**kwargs)[self.index]

    def wait(self, timeout=10, shot_flag=True):
        if self.element.wait(timeout=timeout):
            return True
        else:
            if shot_flag:
                driver.allure_shot(f'元素:{self.element_loc}定位失败')
                raise AssertionError(f'元素:{self.element_loc}定位失败')
            else:
                return False

    # 用于常见分支场景判断
    def exists(self, timeout=1):
        logger.info(f'判断元素是否存在: {self.element_loc}')
        status = self.wait(timeout=timeout, shot_flag=False)
        logger.info(status)
        return status

    def click(self, timeout=10):
        logger.info(f'点击元素: {self.element_loc}')
        if self.wait():
            self.element.click(timeout=timeout)

    # 确保点击后页面会跳转，前提是跳转后的页面没有该元素
    def click_ensure(self, timeout=5):
        self.element.click()
        count = 0
        while count < timeout and self.element.exists(1):
            self.element.click()
            time.sleep(1)
            count += 1

    def send_keys(self, content):
        logger.info(f'定位元素并输入{content}: {self.element_loc}')
        if self.wait():
            self.element.send_keys(content)
            d.send_action('search')
            d.set_fastinput_ime(False)

    def get_text(self):
        logger.info(f'获取元素文本: {self.element_loc}')
        if self.wait():
            return self.element.get_text()
        else:
            return None

