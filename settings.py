import platform
from common import entity

mysql_host = "192.168.11.101"
mysql_port = 3306
mysql_user = "yangcg"
mysql_password = "yangcaogui"

inception_host = "192.168.11.101"
inception_port = 6669
inception_user = "yangcg"
inception_password = "yangcaogui"

LINUX_OS = 'Linux' in platform.system()
WINDOWS_OS = 'Windows' in platform.system()

host_info = entity.Entity()
host_info.host = "192.168.11.101"
host_info.port = 3306
host_info.user = "yangcg"
host_info.password = "yangcaogui"
