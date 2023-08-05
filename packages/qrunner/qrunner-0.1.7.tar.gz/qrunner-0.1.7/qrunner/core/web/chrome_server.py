import os
import subprocess
from utils.log import logger


class ChromeServer:
    @staticmethod
    def launch_server(self):
        logger.info('启动chromedriver')
        p = subprocess.Popen(['chromedriver', '--port={}'.format(9515)])
        try:
            return_code = p.wait(5)
            raise subprocess.CalledProcessError(return_code, p)
        except Exception as e:
            code = e.__dict__.get('returncode')
            if code is None:
                logger.info('chromedriver 启动成功')
            else:
                print(f'chromedriver 启动失败: {e.__dict__}')

    @staticmethod
    def stop_server():
        logger.info('\n停止chromedriver')
        try:
            os.popen('taskkill /f /im chromedriver.exe')
        except Exception as e:
            logger.error(f'停止chromedriver失败: {str(e)}')
        else:
            logger.info('停止chromedriver服务成功')


