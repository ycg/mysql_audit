# -*- coding: utf-8 -*-

from flask import render_template
import inception_util, cache, db_util, settings

def audit_sql(obj):
    if(len(obj.sql) <= 0):
        return "请输入SQL"
    if(obj.host_id <= 0):
        return "请选择审核集群"
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(obj.sql, cache.MyCache().get_mysql_host_info(obj.host_id)))

def get_audit_mysql_host():
    return cache.MyCache().get_mysql_host_info()

def get_execute_mysql_host():
    return cache.MyCache().get_mysql_host_info()

def add_sql_work(obj):
    sql = """INSERT INTO `mysql_audit`.`sql_work`
             (`create_user_id`, `audit_user_id`, `execute_user_id`, `audit_date_time`, `execute_date_time`,
              `mysql_host_id`, `jira_url`, `is_backup`, `backup_table`, `sql_value`, `return_value`, `status`, `title`)
             VALUES
             ({0}, {1}, 0, NULL, NULL, {2}, '{3}', {4}, '', '{5}', '', 0, '{6}');"""\
             .format(obj.current_user_id, obj.dba_user_id, obj.host_id, obj.jira_url, obj.is_backup, obj.sql, obj.title)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)

def delete_sql_work(id):
    db_util.DBUtil().execute(settings.MySQL_HOST, "update `mysql_audit`.`sql_work` set is_deleted = 1 where id={0}".format(id))
    return "delete ok."

def get_sql_list(obj):
    sql = "select * from mysql_audit.sql_work where 1 = 1 order by id desc limit 20;"
    return db_util.DBUtil().get_list_infos(settings.MySQL_HOST, sql)
