import argparse
import pytest
from utils.config import conf


# 获取命令行输入的数据
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--serial_no', dest='serial_no', type=str, default='', help='设备id')
parser.add_argument('p', '--pkg_name', dest='pkg_name', type=str, default='', help='应用包名')
parser.add_argument('-l', '--pkg_url', dest='pkg_url', type=str, default='', help='安装包路径')
parser.add_argument('-i', '--install', dest='install', type=str, default='no', help='是否需要重新安装, yes or no')

# 将数据写入配置文件
args = parser.parse_args()
conf.set_name('device', 'serial_no', args.serial_no)
conf.set_name('app', 'pkg_name', args.pkg_name)
conf.set_name('app', 'need_install', args.install)
conf.set_name('app', 'pkg_url', args.apk_url)

# 执行用例
pytest.main(['tests', '--reruns', '1 ', '-s', '-v', '--alluredir', 'allure-results',
             '--clean-alluredir', '--html=report.html', '--self-contained-html'])
