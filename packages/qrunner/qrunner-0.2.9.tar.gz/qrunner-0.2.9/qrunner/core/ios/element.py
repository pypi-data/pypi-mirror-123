from qrunner.core.ios.driver import Driver
from qrunner.core.ios.driver import relaunch_wda
from qrunner.utils.log import logger


# 初始化driver
driver = Driver()
d = driver.d


class Element:
    def __init__(self, *args, **kwargs):
        self.element_loc = kwargs
        self.xpath = kwargs.get('xpath', '')
        self.index = kwargs.pop('index', '')
        self.element = d.xpath(self.xpath) if self.xpath else d(**kwargs)[self.index]

    @relaunch_wda
    def wait(self, timeout=10, shot_flag=True):
        if self.element.wait(timeout=timeout):
            return True
        else:
            if shot_flag:
                driver.allure_shot(f'元素:{self.element_loc}定位失败')
                raise AssertionError(f'元素:{self.element_loc}定位失败')

    @relaunch_wda
    def exists(self, timeout=1):
        logger.info(f'判断元素是否存在: {self.element_loc}')
        status = self.wait(timeout=timeout, shot_flag=False)
        logger.info(status)
        return status

    @relaunch_wda
    def scroll(self):
        logger.info(f'滚动到元素: {self.element_loc}')
        if self.wait():
            self.element.scroll()

    @relaunch_wda
    def click(self, timeout=10):
        logger.info(f'点击元素: {self.element_loc}')
        if self.wait(timeout=timeout):
            self.element.click()

    @relaunch_wda
    def send_keys(self, content):
        logger.info(f'定位元素: {self.element_loc} ,并输入: {content}')
        if self.wait():
            self.element.clear_text()
            self.element.set_text(content)
            if d(label='Done').exists:
                d(label='Done').click()
            if d(label='搜索').exists:
                d(label='搜索').click()

    @relaunch_wda
    def get_text(self):
        logger.info(f'获取元素文本: {self.element_loc}')
        if self.wait():
            return self.element.text
        else:
            return None

    # 有时候通过text获取不到文本，可以尝试下该方法
    @relaunch_wda
    def get_value(self):
        logger.info(f'获取元素value: {self.element_loc}')
        if self.wait():
            return self.element.value
        else:
            return None

    @relaunch_wda
    def scroll(self):
        logger.info(f'滚动到该元素: {self.element_loc}')
        if self.wait():
            self.element.scroll()



