import time
from qrunner.utils.log import logger
from qrunner.core.android.driver import Driver


# 初始化driver
driver = Driver()
d = driver.d


# 安卓原生元素
class Element:
    def __init__(self,
                 rid=None,
                 className=None,
                 text=None,
                 textContains=None,
                 xpath=None,
                 index=None
                 ):
        self.element_loc = {'resourceId': rid, 'className': className, 'text': text, 'textContains': textContains, 'xpath': xpath, 'index': index}
        self.element_loc = {k: v for k, v in self.element_loc.items() if v is not None}  # 去除为None的定位器
        if xpath:
            self.element = d.xpath(xpath)
        elif rid:
            if text:
                self.element = d(resourceId=rid, text=text)
            elif textContains:
                self.element = d(resourceId=rid, textContains=textContains)
            else:
                logger.info('暂不支持的定位方式')
                raise AssertionError('暂不支持的定位方式')
        elif not rid:
            if text:
                self.element = d(text=text)
            elif textContains:
                self.element = d(textContains=textContains)
            elif className:
                self.element = d(className=className)
            else:
                logger.info('暂不支持的定位方式')
                raise AssertionError('暂不支持的定位方式')
        if index:
            self.element = self.element[index]

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

