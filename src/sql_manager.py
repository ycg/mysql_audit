# -*- coding: utf-8 -*-

import json
from flask import render_template
import inception_util, cache, db_util, settings, common_util

PAGE_SIZE = 10

#根据sql和主机id审核sql
def audit_sql(obj):
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(obj.sql, cache.MyCache().get_mysql_host_info(obj.host_id)))

#根据sql_id获取sql进行审核
def audit_sql_by_sql_id(sql_id):
    sql_info = get_sql_info_by_id(sql_id)
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(sql_info.sql_value, cache.MyCache().get_mysql_host_info(sql_info.mysql_host_id)))

#获取审核的数据库主机信息
def get_audit_mysql_host():
    return cache.MyCache().get_mysql_host_info()

#获取执行的数据库主机信息
def get_execute_mysql_host():
    return cache.MyCache().get_mysql_host_info()

# 添加工单时应该自动审核一下比较好
# 状态 0：未审核 1：已审核 2：审核不通过 3：执行错误 4：执行成功 5：执行中 6：工单已撤销
def add_sql_work(obj):
    result = inception_util.sql_audit(obj.sql, cache.MyCache().get_mysql_host_info(obj.host_id))
    if(get_sql_execute_status(result) == False):
        return "提交的SQL有错误，请仔细检查！"
    status = settings.SQL_AUDIT_OK if (get_sql_execute_status(result)) else settings.SQL_AUDIT_FAIL
    sql = """INSERT INTO `mysql_audit`.`sql_work`
             (`create_user_id`, `audit_user_id`, `execute_user_id`, `audit_date_time`, `execute_date_time`,
              `mysql_host_id`, `jira_url`, `is_backup`, `backup_table`, `sql_value`, `return_value`, `status`, `title`)
             VALUES
             ({0}, {1}, {1}, NULL, NULL, {2}, '{3}', {4}, '', '{5}', '', {6}, '{7}');""" \
        .format(obj.current_user_id, obj.dba_user_id, obj.host_id, obj.jira_url, obj.is_backup, db_util.DBUtil().escape(obj.sql), status, obj.title)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    return "提交SQL工单成功"

# 根据id删除工单
def delete_sql_work(id):
    db_util.DBUtil().execute(settings.MySQL_HOST, "update `mysql_audit`.`sql_work` set is_deleted = 1 where id = {0}".format(id))
    return "delete ok."

# 根据查询条件获取工单列表-有分页功能
def get_sql_list(obj):
    sql = """select t1.id, t1.title, t1.create_user_id, t1.audit_user_id, t1.execute_user_id, t1.audit_date_time,
                    t1.execute_date_time, t1.mysql_host_id, t1.jira_url, if(t1.is_backup = 0, 'No', 'Yes') as is_backup,
                    t1.backup_table, left(sql_value, 50) as sql_value, t1.return_value, t1.status, t1.is_deleted, t1.created_time,
                    t2.host_name, t3.chinese_name, ifnull(t4.chinese_name, '') as execute_user_name
             from mysql_audit.sql_work t1
             left join `mysql_audit`.mysql_hosts t2 on t1.mysql_host_id = t2.host_id
             left join mysql_audit.work_user t3 on t1.create_user_id = t3.user_id
             left join mysql_audit.work_user t4 on t1.execute_user_id = t4.user_id
             where 1 = 1 order by t1.id desc limit {0}, {1};"""
    sql = sql.format((obj.page_number - 1) * settings.SQL_LIST_PAGE_SIZE, settings.SQL_LIST_PAGE_SIZE)
    result_list = db_util.DBUtil().get_list_infos(settings.MySQL_HOST, sql)
    for info in result_list:
        get_sql_work_status_name(info)
    return result_list

# 根据工单id获取全部信息
def get_sql_info_by_id(id):
    sql = """select t1.sql_value, t1.title, t1.jira_url, t1.execute_user_id, t1.is_backup,
             t2.host_name, t3.chinese_name, t1.mysql_host_id, t1.id, t1.status, t1.return_value
             from `mysql_audit`.`sql_work` t1
             left join `mysql_audit`.mysql_hosts t2 on t1.mysql_host_id = t2.host_id
             left join mysql_audit.work_user t3 on t1.create_user_id = t3.user_id
             where t1.id = {0};""".format(id)
    return get_sql_work_status_name(common_util.get_object(db_util.DBUtil().fetchone(settings.MySQL_HOST, sql)))

# 执行sql并更新工单状态
# 状态 0：未审核 1：已审核 2：审核不通过 3：执行错误 4：执行成功
def sql_execute(sql_id):
    sql_info = get_sql_info_by_id(sql_id)
    if (sql_info.status == settings.SQL_EXECUTE_SUCCESS):
        return json.loads(sql_info.return_value)
    else:
        result_obj = inception_util.sql_execute(sql_info.sql_value,
                                                cache.MyCache().get_mysql_host_info(sql_info.mysql_host_id),
                                                is_backup=sql_info.is_backup)
        sql = "update mysql_audit.sql_work set return_value = '{0}', `status` = {1} where id = {2};" \
            .format(db_util.DBUtil().escape(json.dumps(result_obj, default=lambda o: o.__dict__)),
                    settings.SQL_EXECUTE_SUCCESS if (get_sql_execute_status(result_obj)) else settings.SQL_EXECUTE_FAIL,
                    sql_info.id)
        db_util.DBUtil().execute(settings.MySQL_HOST, sql)
        return result_obj

# 获取执行成功的SQL执行结果
def get_sql_result(sql_id):
    return json.loads(get_sql_info_by_id(sql_id).return_value)

#获取sql执行状态的中文
#状态 0：未审核 1：已审核 2：审核不通过 3：执行错误 4：执行成功 5：执行中 6：工单已撤销
def get_sql_work_status_name(sql_info):
    if (sql_info.status == settings.SQL_NO_AUDIT):
        sql_info.status_name = "未审核"
    elif (sql_info.status == settings.SQL_AUDIT_OK):
        sql_info.status_name = "审核成功"
    elif (sql_info.status == settings.SQL_AUDIT_FAIL):
        sql_info.status_name = "审核错误"
    elif (sql_info.status == settings.SQL_EXECUTE_FAIL):
        sql_info.status_name = "执行错误"
    elif (sql_info.status == settings.SQL_EXECUTE_SUCCESS):
        sql_info.status_name = "执行成功"
    elif (sql_info.status == settings.SQL_EXECUTE_ING):
        sql_info.status_name = "执行中..."
    elif (sql_info.status == settings.SQL_WORK_CANCEL):
        sql_info.status_name = "工单已撤销"
    return sql_info

# 获取sql审核或执行的状态
# True：执行或审核没有错误
# False：执行或审核出现严重错误
def get_sql_execute_status(result):
    for info in result:
        if (info.errlevel == settings.INCETION_SQL_ERROR):
            return False
    return True
