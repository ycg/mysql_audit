import platform
from src import common_util

inception_host = "192.168.11.101"
inception_port = 6669
inception_user = "yangcg"
inception_password = "yangcaogui"

LINUX_OS = 'Linux' in platform.system()
WINDOWS_OS = 'Windows' in platform.system()

MySQL_HOST = common_util.Entity()
MySQL_HOST.key = 99999
MySQL_HOST.host = "192.168.11.101"
MySQL_HOST.port = 3306
MySQL_HOST.user = "yangcg"
MySQL_HOST.password = "yangcaogui"
