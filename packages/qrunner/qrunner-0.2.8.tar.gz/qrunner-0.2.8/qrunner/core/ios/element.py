from qrunner.core.ios.driver import Driver
from qrunner.core.ios.driver import relaunch_wda
from qrunner.utils.log import logger


# 初始化driver
driver = Driver()
d = driver.d


class Element:
    def __init__(self, name=None,
                 nameContains=None,
                 value=None,
                 valueContains=None,
                 xpath=None,
                 index=None,
                 label=None,
                 labelContains=None,
                 className=None):
        self.element_loc = {
            'name': name,
            'nameContains': nameContains,
            'value': value,
            'valueContains': valueContains,
            'xpath': xpath,
            'label': label,
            'labelContains': labelContains,
            'className': className,
            'index': index
        }
        self.element_loc = {k: v for k, v in self.element_loc.items() if v is not None}  # 去除为None的定位器
        if xpath and name:
            self.element = d(xpath=xpath, name=name)
        elif xpath and nameContains:
            self.element = d(xpath=xpath, nameContains=nameContains)
        elif name and className:
            self.element = d(name=name, className=className)
        else:
            if xpath:
                self.element = d(xpath=xpath)
            elif name:
                self.element = d(name=name)
            elif nameContains:
                self.element = d(nameContains=nameContains)
            elif label:
                self.element = d(label=label)
            elif labelContains:
                self.element = d(labelContains=labelContains)
            elif value:
                self.element = d(value)
            elif valueContains:
                self.element = d(valueContains=valueContains)
            elif className:
                self.element = d(className=className)
            else:
                logger.info('暂不支持的定位方式')
        if index:
            self.element = self.element[index]

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
            d(label='Done').click()

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



