# -*- coding: utf-8 -*-

import json, traceback
import settings, cache, db_util, common_util, custom_algorithm


def query_host_infos():
    return cache.MyCache().get_mysql_host_info()


def add(obj):
    sql = "select host_id from mysql_audit.mysql_hosts where ip = '{0}' and port = {1};".format(obj.host_ip, obj.host_port)
    result = db_util.DBUtil().fetchone(settings.MySQL_HOST, sql)
    if (result is not None):
        return "1"

    is_alive = test_connection_new(obj)
    sql = """insert into mysql_audit.mysql_hosts
             (ip, port, `user`, `password`, host_name, is_alive)
             VALUES
             ('{0}', {1}, '{2}', '{3}', '{4}', {5})""" \
        .format(obj.host_ip,
                obj.host_port,
                custom_algorithm.encrypt(settings.MY_KEY, obj.host_user),
                custom_algorithm.encrypt(settings.MY_KEY, obj.host_password),
                obj.host_name, is_alive)
    db_util.DBUtil().fetchone(settings.MySQL_HOST, sql)
    cache.MyCache().load_mysql_host_infos()
    return "2"


def update(obj):
    sql = "select ip, port, `user`, `password`, host_name from mysql_audit.mysql_hosts where host_id = {0}".format(obj.host_id)
    info = common_util.get_object(db_util.DBUtil().fetchone(settings.MySQL_HOST, sql))
    return json.dumps(info, default=lambda o: o.__dict__)


def delete(obj):
    sql = "delete from mysql_audit.mysql_hosts where host_id = {0};".format(obj.host_id)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    cache.MyCache().delete_host_info_by_host_id(obj.host_id)


def test_connection(obj):
    result = test_connection_new(obj)
    if (result):
        return "连接成功!"
    return "连接失败!"


def test_connection_new(obj):
    try:
        db_util.DBUtil().execute_sql(obj.host_ip, obj.host_port, obj.host_user, obj.host_password, "select 1;")
    except Exception:
        traceback.print_exc()
        return False
    return True


def get_host_info(obj):
    sql = "select ip, port, `user`, `password`, host_name from mysql_audit.mysql_hosts where host_id = {0}".format(obj.host_id)
    info = common_util.get_object(db_util.DBUtil().fetchone(settings.MySQL_HOST, sql))
    info.user = custom_algorithm.decrypt(settings.MY_KEY, info.user)
    return json.dumps(info, default=lambda o: o.__dict__)
