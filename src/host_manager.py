# -*- coding: utf-8 -*-

import traceback, json
import settings, cache, db_util, common_util

def query_host_infos(obj):
    result = cache.MyCache().get_mysql_host_info(host_id=obj.host_id)
    if(obj.host_type > 0):
        pass
    if(len(obj.host_name) > 0):
        pass
    return result


def add(obj):
    sql = """insert into mysql_audit.mysql_hosts
             (ip, port, `user`, `password`, host_name)
             VALUES
             ({0}, {1}, {2}, {3}, {4})""".format(obj.host_ip, obj.host_port, obj.host_user, obj.host_password, obj.host_name)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    cache.MyCache().load_mysql_host_infos()

def update(obj):
    sql = "select ip, port, `user`, `password`, host_name from mysql_audit.mysql_hosts where host_id = {0}".format(obj.host_id)
    info = common_util.get_object(db_util.DBUtil().fetchone(settings.MySQL_HOST, sql))
    return json.dumps(info, default=lambda o: o.__dict__)

def delete(obj):
    sql = "update mysql_audit.mysql_hosts set is_deleted = 1 where host_id = {0};".format(obj.host_id)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    cache.MyCache().load_mysql_host_infos()

def test_connection(obj):
    try:
        db_util.DBUtil().execute_sql(obj.host_ip, obj.host_port, obj.host_user, obj.host_password, "select 1;")
    except Exception:
        traceback.print_exc()
        return "连接失败!"
    return "连接成功!"

def get_host_info(obj):
    sql = "select ip, port, `user`, `password`, host_name from mysql_audit.mysql_hosts where host_id = {0}".format(obj.host_id)
    info = common_util.get_object(db_util.DBUtil().fetchone(settings.MySQL_HOST, sql))
    return json.dumps(info, default=lambda o: o.__dict__)

