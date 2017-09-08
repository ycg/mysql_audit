# -*- coding: utf-8 -*-

import platform
from src.custom_entity import Entity

inception_host = "192.168.11.101"
inception_port = 6669
inception_user = "yangcg"
inception_password = "yangcaogui"

LINUX_OS = 'Linux' in platform.system()
WINDOWS_OS = 'Windows' in platform.system()

MySQL_HOST = Entity()
MySQL_HOST.key = 99999
MySQL_HOST.host = "192.168.11.101"
MySQL_HOST.port = 3306
MySQL_HOST.user = "yangcg"
MySQL_HOST.password = "yangcaogui"

THREAD_POOL_SIZE = 20

ROLE_DEV = 1000
ROLE_LEADER = 1001
ROLE_ADMINISTRATOR = 1002

DBA_GROUP_ID = 10000

SQL_NO_AUDIT = 0
SQL_AUDIT_OK = 1
SQL_AUDIT_FAIL = 2
SQL_EXECUTE_FAIL = 3
SQL_EXECUTE_SUCCESS = 4
SQL_EXECUTE_ING = 5
SQL_WORK_CANCEL = 6
SQL_WORK_ROLLBACK = 7

INCETION_SQL_OK = 0
INCETION_SQL_WARNING = 1
INCETION_SQL_ERROR = 2

SQL_LIST_PAGE_SIZE = 15

SQL_WORK_STATUS_DICT = {
    SQL_NO_AUDIT: "未审核",
    SQL_AUDIT_OK: "审核成功",
    SQL_AUDIT_FAIL: "审核失败",
    SQL_EXECUTE_FAIL: "执行错误",
    SQL_EXECUTE_SUCCESS: "执行成功",
    SQL_EXECUTE_ING: "执行中",
    SQL_WORK_CANCEL: "取消工单",
    SQL_WORK_ROLLBACK: "工单已回滚"
}

EMAIL_HOST = ""
EMAIL_PORT = 25
EMAIL_USER = ""
EMAIL_PASSWORD = ""
EMAIL_SEND_USERS = ""
EMAIL_SEND_ENABLE = False

MY_KEY = 20

