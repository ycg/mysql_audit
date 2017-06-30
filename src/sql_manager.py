# -*- coding: utf-8 -*-

from flask import render_template
import inception_util, cache, db_util, settings, common_util

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

#添加工单时应该自动审核一下比较好
def add_sql_work(obj):
    status = 2
    result = inception_util.sql_audit(obj.sql, cache.MyCache().get_mysql_host_info(obj.host_id))
    for info in result:
        if(info.errlevel == 2):
            status = 3
    sql = """INSERT INTO `mysql_audit`.`sql_work`
             (`create_user_id`, `audit_user_id`, `execute_user_id`, `audit_date_time`, `execute_date_time`,
              `mysql_host_id`, `jira_url`, `is_backup`, `backup_table`, `sql_value`, `return_value`, `status`, `title`)
             VALUES
             ({0}, {1}, 0, NULL, NULL, {2}, '{3}', {4}, '', '{5}', '', {6}, '{7}');"""\
             .format(obj.current_user_id, obj.dba_user_id, obj.host_id, obj.jira_url, obj.is_backup, db_util.DBUtil().escape(obj.sql), status, obj.title)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)

#根据id删除工单
def delete_sql_work(id):
    db_util.DBUtil().execute(settings.MySQL_HOST, "update `mysql_audit`.`sql_work` set is_deleted = 1 where id={0}".format(id))
    return "delete ok."

#根据查询条件获取工单列表-有分页功能
def get_sql_list(obj):
    sql = """select t1.id, t1.title, t1.create_user_id, t1.audit_user_id, t1.execute_user_id, t1.audit_date_time,
                    t1.execute_date_time, t1.mysql_host_id, t1.jira_url, if(t1.is_backup = 0, '否', '是') as is_backup, t1.backup_table, left(sql_value, 50) as sql_value, t1.return_value, t1.status, t1.is_deleted, t1.created_time,
                    t2.host_name, t3.chinese_name
             from mysql_audit.sql_work t1
             left join `mysql_audit`.mysql_hosts t2 on t1.mysql_host_id = t2.host_id
             left join mysql_audit.work_user t3 on t1.create_user_id = t3.user_id
             where 1 = 1 order by t1.id desc limit 20;"""
    return db_util.DBUtil().get_list_infos(settings.MySQL_HOST, sql)

#根据工单id获取全部信息
def get_sql_info_by_id(id):
    sql = """select t1.sql_value, t1.title, t1.jira_url, t1.is_backup, t2.host_name, t3.chinese_name
             from `mysql_audit`.`sql_work` t1
             left join `mysql_audit`.mysql_hosts t2 on t1.mysql_host_id = t2.host_id
             left join mysql_audit.work_user t3 on t1.create_user_id = t3.user_id
             where t1.id = {0};""".format(id)
    return common_util.get_object(db_util.DBUtil().fetchone(settings.MySQL_HOST, sql))
