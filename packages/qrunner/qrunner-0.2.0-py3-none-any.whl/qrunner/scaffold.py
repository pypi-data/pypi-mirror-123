import os.path
import subprocess
import sys
from qrunner.utils.log import logger


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_parser_scaffold.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ create scaffold with specified project name.
    """

    def show_tree(prj_name):
        try:
            print(f"\n$ tree {prj_name} -a")
            subprocess.run(["tree", prj_name, "-a"])
            print("")
        except FileNotFoundError:
            logger.warning("tree command not exists, ignore.")

    if os.path.isdir(project_name):
        logger.warning(
            f"Project folder {project_name} exists, please specify a new project name."
        )
        show_tree(project_name)
        return 1
    elif os.path.isfile(project_name):
        logger.warning(
            f"Project name {project_name} conflicts with existed file, please specify a new one."
        )
        return 1

    logger.info(f"Create new project: {project_name}")
    print(f"Project Root Dir: {os.path.join(os.getcwd(), project_name)}\n")

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    demo_run = """
import argparse
import pytest
from conf.config import conf


# 获取命令行输入的数据
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--serial_no', dest='serial_no', type=str, default='', help='设备id')
parser.add_argument('-p', '--pkg_name', dest='pkg_name', type=str, default='', help='应用包名')
parser.add_argument('-l', '--pkg_url', dest='pkg_url', type=str, default='', help='安装包路径')
parser.add_argument('-i', '--install', dest='install', type=str, default='no', help='是否需要重新安装, yes or no')

# 将数据写入配置文件
args = parser.parse_args()
conf.set_name('device', 'serial_no', args.serial_no)
conf.set_name('app', 'pkg_name', args.pkg_name)
conf.set_name('app', 'need_install', args.install)
conf.set_name('app', 'pkg_url', args.pkg_url)

# 执行用例
pytest.main(['tests', '--reruns', '1 ', '-s', '-v', '--alluredir', 'allure-results',
             '--clean-alluredir', '--html=report.html', '--self-contained-html'])
"""
    demo_conftest = """
import pytest
from qrunner.core.android.element import driver, Element as E
from qrunner.utils.log import logger
from conf.config import conf


# 安装应用
@pytest.fixture(scope='session', autouse=True)
def install_app():
    if conf.get_name('app', 'need_install') == 'yes':
        pkg_url = conf.get_name('app', 'pkg_url')
        logger.info(f'安装应用: {pkg_url}')
        driver.install_app(pkg_url, is_new=True)
    else:
        logger.info('无需重装应用')


# 初始化应用
@pytest.fixture(scope='session', autouse=True)
def init_app(install_app):
    if conf.get_name('app', 'need_install') == 'yes':
        pass
    else:
        logger.info('无需初始化')


# 用例的前置和后置操作
@pytest.fixture(scope='function', autouse=True)
def init_case():
    # 启动应用
    logger.info('启动应用')
    driver.force_start_app()
    yield
    # 截图
    driver.allure_shot('用例结束')
    # 停止应用
    logger.info('停止应用')
    driver.stop_app()
"""
    demo_page = """
from qrunner.core.android.element import Element, driver


class HomePage:
    bottom_peer = Element(rid='com.qizhidao.clientapp:id/icon2')

    def go_peer(self):
        self.bottom_peer.click()
        driver.allure_shot('查同行')
"""
    demo_case = """
import allure
from pages.demo_page import HomePage


@allure.feature('首页信息流')
@allure.story('金刚位')
class TestPeerSearch:
    @allure.title('从首页信息流进入查同行')
    def test(self):
        HomePage().go_peer()
"""
    ignore_content = "\n".join(
        [".env", "allure-results/*", "__pycache__/*", "*.pyc", ".python-version", "logs/*", "report.html", ".idea/*"]
    )

    config_content = """
[device]
serial_no = 

[app]
need_install = no
pkg_name = 
pkg_url = 
"""
    config_handle = """
import os
import pathlib
import configparser

local_path = os.path.dirname(os.path.realpath(__file__))


class Config:
    def __init__(self):
        self.conf_file_path = os.path.join(local_path, 'config.ini')
        config_file = pathlib.Path(self.conf_file_path)
        config_file.touch(exist_ok=True)
        self.cf = configparser.ConfigParser()
        self.cf.read(self.conf_file_path, encoding='utf-8')

    def get_name(self, module, key):
        if not self.cf.has_option(module, key):
            print('未找到该数据')
            value = None
        else:
            value = self.cf.get(module, key)
        return value

    def set_name(self, module, key, value):
        if not self.cf.has_section(module):
            self.cf.add_section(module)
        self.cf.set(module, key, value)
        with open(self.conf_file_path, 'w') as f:
            self.cf.write(f)


# 初始化
conf = Config()
"""

    create_folder(project_name)
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "pages"))
    create_folder(os.path.join(project_name, "conf"))

    create_file(
        os.path.join(project_name, "tests", "conftest.py"),
        demo_conftest,
    )
    create_file(
        os.path.join(project_name, "tests", "test_demo.py"),
        demo_case,
    )
    create_file(
        os.path.join(project_name, "pages", "demo_page.py"),
        demo_page,
    )
    create_file(
        os.path.join(project_name, "conf", "config.ini"),
        config_content,
    )
    create_file(
        os.path.join(project_name, "conf", "config.py"),
        config_handle,
    )
    create_file(
        os.path.join(project_name, "run.py"),
        demo_run,
    )
    create_file(
        os.path.join(project_name, ".gitignore"),
        ignore_content,
    )

    show_tree(project_name)
    return 0


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

