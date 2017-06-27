# -*- coding: utf-8 -*-

#强大的查询条件
#要根据权限的不同显示不同的菜单

#查询条件有
#按照用户id，时间，安装执行状态

import settings
from common import db_util

def get_sql_list(obj):
    sql = "select * from mysql_audit.sql_work where 1 = 1 order by id desc limit 20;"
    return db_util.DBUtil().get_list_infos(settings.MySQL_HOST, sql)

def get_user_list():
    pass

def get_mysql_host_list():
    pass

