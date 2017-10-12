# -*- coding: utf-8 -*-

import json, time, traceback
from flask import render_template, request
import inception_util, cache, db_util, settings, common_util, custom_entity


# 根据sql和主机id审核sql
def audit_sql(obj):
    obj.sql = get_use_db_sql(obj.sql, obj.db_name)
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(obj.sql, cache.MyCache().get_mysql_host_info(obj.host_id)))


# 根据sql_id获取sql进行审核
def audit_sql_by_sql_id(sql_id):
    sql_info = get_sql_info_by_id(sql_id)
    sql_info.sql_value = get_use_db_sql(sql_info.sql_value, sql_info.execute_db_name)
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(sql_info.sql_value, cache.MyCache().get_mysql_host_info(sql_info.mysql_host_id)))


# 审核sql是否能执行
# 做的好一点话，如果审核不通过需要写明理由
def audit_sql_work(obj):
    status = settings.SQL_AUDIT_OK if (obj.status) else settings.SQL_AUDIT_FAIL
    sql = """update `mysql_audit`.`sql_work` set `status` = {0}, remark = '{1}' where id = {2};""".format(status, obj.remark, obj.sql_id)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    return "操作成功"


# 获取审核的数据库主机信息
def get_audit_mysql_host():
    return cache.MyCache().get_mysql_host_info()


# 获取执行的数据库主机信息
def get_execute_mysql_host():
    return cache.MyCache().get_mysql_host_info()


# 添加工单时应该自动审核一下比较好
# 状态 0：未审核 1：已审核 2：审核不通过 3：执行错误 4：执行成功 5：执行中 6：工单已撤销
def add_sql_work(obj):
    try:
        audit_result = inception_util.sql_audit(get_use_db_sql(obj.sql_value, obj.db_name), cache.MyCache().get_mysql_host_info(obj.host_id))
        if (get_sql_execute_status(audit_result) == False):
            return "提交的SQL有错误，请审核之后在提交！"

        user_info = cache.MyCache().get_user_info(obj.current_user_id)
        sql = """INSERT INTO `mysql_audit`.`sql_work`
                 (`create_user_id`, `audit_user_id`, `audit_date_time`, `execute_date_time`,
                  `mysql_host_id`, `jira_url`, `is_backup`, `backup_table`, `sql_value`,
                  `return_value`, `status`, `title`, `audit_result_value`, `execute_db_name`, `create_user_group_id`, sleep,
                  `create_user_name`, `audit_user_name`, `execute_user_name`, `execute_user_id`)
                 VALUES
                 ({0}, {1}, NOW(), NULL, {2}, '{3}', {4}, '', '{5}', '', {6}, '{7}', '{8}', '{9}', {10}, {11}, '{12}', '{13}', '{14}', {15});""" \
            .format(obj.current_user_id,
                    obj.audit_user_id,
                    obj.host_id,
                    db_util.DBUtil().escape(str(obj.jira_url)),
                    obj.is_backup,
                    db_util.DBUtil().escape(obj.sql_value),
                    settings.SQL_NO_AUDIT,
                    db_util.DBUtil().escape(str(obj.title)),
                    db_util.DBUtil().escape(json.dumps(audit_result, default=lambda o: o.__dict__)),
                    obj.db_name,
                    user_info.group_id,
                    obj.sleep_time,
                    user_info.chinese_name,
                    cache.MyCache().get_user_chinese_name(obj.audit_user_id),
                    cache.MyCache().get_user_chinese_name(obj.dba_user_id),
                    obj.dba_user_id)
        db_util.DBUtil().execute(settings.MySQL_HOST, sql)
        return "创建SQL工单成功"
    except Exception, e:
        traceback.print_exc()
        return e.message


# 增加编辑未执行的工单功能
# 修改标题，jira地址，是否备份，执行sql的DBA
# sql和上线的库为什么不可以修改，主要是如果你写错了，那么审核的时候肯定就不通过的
def update_sql_work(obj):
    sql = """update `mysql_audit`.`sql_work`
             set `title` = '{0}', `jira_url` = '{1}', `execute_user_id` = {2},
                 is_backup = {3}, sleep = {4}, `execute_user_name` = '{5}', audit_user_id = {6}, audit_user_name = '{7}'
             where id = {8};""".format(db_util.DBUtil().escape(str(obj.title)),
                                       db_util.DBUtil().escape(str(obj.jira_url)),
                                       obj.dba_user_id,
                                       obj.is_backup,
                                       obj.sleep_time,
                                       cache.MyCache().get_user_chinese_name(obj.dba_user_id),
                                       obj.audit_user_tmp,
                                       cache.MyCache().get_user_chinese_name(obj.audit_user_tmp),
                                       obj.sql_id)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    return "update ok."


# 根据id删除工单
def delete_sql_work(sql_id):
    db_util.DBUtil().execute(settings.MySQL_HOST, "update `mysql_audit`.`sql_work` set is_deleted = 1 where id = {0}".format(sql_id))
    return "delete ok."


# 根据查询条件获取工单列表-有分页功能
# admin用户查询工单列表的接口，其它用户不掉用
def get_sql_list(obj):
    sql_where = ""
    obj.tab_type = 0
    if (int(obj.status) >= 0):
        sql_where += " and status = {0}".format(obj.status)
    if (int(obj.user_id) > 0):
        sql_where += " and create_user_id = {0}".format(obj.user_id)
    if (len(obj.start_datetime) > 0):
        sql_where += " and created_time >= '{0}'".format(obj.start_datetime)
    if (len(obj.stop_datetime) > 0):
        sql_where += " and created_time <= '{0}'".format(obj.stop_datetime)
    return get_sql_work_list_by_where(obj, sql_where)


# 根据工单id获取全部信息
def get_sql_info_by_id(id):
    sql = """select t1.sql_value, t1.title, t1.jira_url, t1.execute_user_id, t1.is_backup, t1.sleep, t1.audit_user_id,
                    t1.ignore_warnings, rollback_sql, execute_date_time, t2.host_name, t1.mysql_host_id, t1.id, t1.status,
                    t1.return_value, t1.execute_db_name, t1.audit_result_value, t1.execute_user_id, t1.created_time,
                    create_user_name, audit_user_name, execute_user_name, real_execute_user_name
             from `mysql_audit`.`sql_work` t1
             left join `mysql_audit`.mysql_hosts t2 on t1.mysql_host_id = t2.host_id where t1.id = {0};""".format(id)
    return get_sql_work_status_name(common_util.get_object(db_util.DBUtil().fetchone(settings.MySQL_HOST, sql)))


# 执行sql并更新工单状态
# 状态 0：未审核 1：已审核 2：审核不通过 3：执行错误 4：执行成功
def sql_execute(obj):
    try:
        return_info = custom_entity.Entity()
        return_info.message = ""
        return_info.execute_result = None
        sql_info = get_sql_info_by_id(obj.sql_id)
        user_info = cache.MyCache().get_user_info(obj.current_user_id)

        if (user_info.group_id != settings.ADMIN_GROUP_ID):
            # 如果审核没通过，或者审核失败，也不允许执行
            if (sql_info.status == settings.SQL_NO_AUDIT or sql_info.status == settings.SQL_AUDIT_FAIL):
                return_info.message = "审核不通过，不允许执行！"
            # 如果工单指定执行的用户跟实际执行的用户不一样，那不允许通过
            elif (sql_info.execute_user_id != user_info.user_id):
                return_info.message = "你不能执行此工单，该工单指定执行用户不是你！"
        elif (sql_info.status == settings.SQL_EXECUTE_ING):
            # 如果工单正在执行中，不允许重复执行SQL
            return_info.message = "SQL工单正在执行中，请耐心等待..."
        elif (sql_info.status == settings.SQL_EXECUTE_SUCCESS):
            # 如果已经执行成功，直接返回执行结果
            return_info.execute_result = json.loads(sql_info.return_value)
        else:
            # 更新工单状态为执行中
            sql = "update mysql_audit.sql_work set `status` = {0}, `execute_start_date_time` = NOW(), `execute_date_time` = NOW() where id = {1};".format(settings.SQL_EXECUTE_ING, sql_info.id)
            db_util.DBUtil().execute(settings.MySQL_HOST, sql)

            if (len(sql_info.execute_db_name.strip()) > 0):
                sql_info.sql_value = "use {0};{1}".format(sql_info.execute_db_name, sql_info.sql_value)
            result_obj = inception_util.sql_execute(sql_info.sql_value,
                                                    cache.MyCache().get_mysql_host_info(sql_info.mysql_host_id),
                                                    is_backup=sql_info.is_backup,
                                                    ignore_warnings=True if (obj.ignore_warnings.upper() == "TRUE") else False,
                                                    sleep_time=sql_info.sleep)
            sql = """update mysql_audit.sql_work
                     set
                     return_value = '{0}',
                     `status` = {1},
                     `ignore_warnings` = {2},
                     `execute_finish_date_time` = NOW(),
                     `real_execute_user_id` = {3},
                     `real_execute_user_name` = '{4}' where id = {5};""".format(db_util.DBUtil().escape(json.dumps(result_obj, default=lambda o: o.__dict__)),
                                                                                settings.SQL_EXECUTE_SUCCESS if (get_sql_execute_status(result_obj)) else settings.SQL_EXECUTE_FAIL,
                                                                                obj.ignore_warnings,
                                                                                obj.current_user_id,
                                                                                cache.MyCache().get_user_info(obj.current_user_id).chinese_name,
                                                                                sql_info.id)
            db_util.DBUtil().execute(settings.MySQL_HOST, sql)
            send_mail_for_execute_success(sql_info.id)
            return_info.execute_result = result_obj
    except Exception, e:
        # 出现异常要更新状态，直接把状态变为fail
        sql = "update mysql_audit.sql_work set `status` = {0} where id = {1};".format(settings.SQL_EXECUTE_FAIL, sql_info.id)
        db_util.DBUtil().execute(settings.MySQL_HOST, sql)
        traceback.print_exc()
        return_info.message = "执行时出现异常，请联系管理员！"
    return return_info


# 停止正在执行的sql
def stop_sql_execute(obj):
    pass


# 如果审核结果有warning，那么要提示用户选择忽视警告执行SQL
def check_sql_audit_result_has_warnings(sql_id):
    result = common_util.Entity()
    sql_info = get_sql_info_by_id(sql_id)
    for info in json.loads(sql_info.audit_result_value):
        obj = common_util.get_object(info)
        if (obj.errlevel == settings.INCETION_SQL_WARNING):
            result.has_warnings = True
            break
        else:
            result.has_warnings = False
    return json.dumps(result, default=lambda o: o.__dict__)


# 获取执行成功的SQL执行结果
def get_sql_result(sql_id):
    sql_info = get_sql_info_by_id(sql_id)
    # 根据状态返回相应的结果，审核状态返回审核结果，执行状态返回执行结果
    if (sql_info.status == settings.SQL_NO_AUDIT or sql_info.status == settings.SQL_AUDIT_OK or sql_info.status == settings.SQL_AUDIT_FAIL):
        return render_template("audit_view.html", audit_infos=json.loads(sql_info.audit_result_value))
    elif (sql_info.status == settings.SQL_EXECUTE_ING or sql_info.status == settings.SQL_EXECUTE_FAIL or sql_info.status == settings.SQL_EXECUTE_SUCCESS):
        return_info = custom_entity.Entity()
        return_info.execute_result = json.loads(sql_info.return_value)
        return render_template("sql_execute_view.html", audit_infos=return_info)


# 获取sql执行状态的中文
# 状态 0：未审核 1：已审核 2：审核不通过 3：执行错误 4：执行成功 5：执行中 6：工单已撤销
def get_sql_work_status_name(sql_info):
    sql_info.status_name = settings.SQL_WORK_STATUS_DICT[sql_info.status]
    return sql_info


# 获取sql审核或执行的状态
# True：执行或审核没有错误
# False：执行或审核出现严重错误
def get_sql_execute_status(result):
    for info in result:
        if (info.errlevel == settings.INCETION_SQL_ERROR):
            return False
    return True


# 获取审核或执行结果是否有警告状态
def get_sql_result_has_warning_status(result):
    for info in result:
        if (info.errlevel == settings.INCETION_SQL_WARNING):
            return False
    return True


# 获取对应数据库的所以库名称
def get_database_names(host_id):
    html_str = """<select id="db_name" name="db_name" class="selectpicker show-tick form-control bs-select-hidden">
                      <option value="0" disabled selected style="color: black">请选择要执行的库:</option>
                      {0}
                  </select>"""
    options_str = ""
    result = db_util.DBUtil().get_list_infos(cache.MyCache().get_mysql_host_info(host_id=host_id), "show databases;")
    for num in range(0, len(result)):
        db_name = result[num].Database;
        # 过滤掉系统库
        if (db_name != "information_schema" and db_name != "mysql" and db_name != "sys" and db_name != "performance_schema"):
            options_str += "<option value=\"{0}\">{1}</option>".format(db_name, db_name)
    return html_str.format(options_str)


# 获取使用use db的完整sql
def get_use_db_sql(sql_value, db_name):
    if (db_name != None):
        return "use {0};{1}".format(db_name, sql_value)
    return sql_value


# 查看回滚SQL语句
def get_rollback_sql(sql_id):
    aa = time.time()
    result = common_util.Entity()
    sql_info = get_sql_info_by_id(sql_id)
    result.rollback_sql = []
    result.rollback_sql_value = ""
    result.is_backup = sql_info.is_backup
    result.host_id = sql_info.mysql_host_id
    if (sql_info.is_backup):
        if (sql_info.rollback_sql != None):
            result.rollback_sql_value = sql_info.rollback_sql
        else:
            for info in json.loads(sql_info.return_value):
                info = common_util.get_object(info)
                if (info.backup_dbname == None):
                    continue
                sql = "select schema_name from information_schema.SCHEMATA where schema_name = '{0}';".format(info.backup_dbname)
                db_name = db_util.DBUtil().fetchone(settings.MySQL_HOST, sql)
                if (db_name == None):
                    continue
                sql = "select tablename from {0}.$_$Inception_backup_information$_$ where opid_time = {1}".format(info.backup_dbname, info.sequence)
                table_name_dict = db_util.DBUtil().fetchone(settings.MySQL_HOST, sql)
                if (table_name_dict == None):
                    continue
                sql = "select rollback_statement from {0}.{1} where opid_time = {2}".format(info.backup_dbname, table_name_dict["tablename"], info.sequence)
                for list_dict in db_util.DBUtil().fetchall(settings.MySQL_HOST, sql):
                    result.rollback_sql.append(list_dict.values()[0])
    bb = time.time()
    print(">>>>>>>>>>>>>>get rollback sql time:{0}<<<<<<<<<<<<<<<<<<<".format(bb - aa))
    if (len(result.rollback_sql) > 0):
        result.rollback_sql_value = "\n".join(result.rollback_sql)
        result.rollback_sql = []
        db_util.DBUtil().execute(settings.MySQL_HOST,
                                 "update mysql_audit.sql_work set `rollback_sql` = '{0}' where id = {1};".format(db_util.DBUtil().escape(result.rollback_sql_value), sql_id))
    return result


# 执行回滚语句
def execute_rollback_sql(sql_id):
    sql_info = get_sql_info_by_id(sql_id)
    rollback_host = cache.MyCache().get_mysql_host_info(int(sql_info.mysql_host_id))
    rollback_sql = "start transaction; " + get_rollback_sql(sql_id).rollback_sql_value + " commit;"
    if (db_util.DBUtil().execute(rollback_host, rollback_sql)):
        db_util.DBUtil().execute(settings.MySQL_HOST, "update mysql_audit.sql_work set `status` = {0} where id = {1};".format(settings.SQL_WORK_ROLLBACK, sql_id))
        return "回滚成功"
    return "回滚失败"


# 审核成功发送邮件
def send_mail_for_audit_success():
    if (settings.EMAIL_SEND_ENABLE):
        pass


# 执行成功发送邮件
def send_mail_for_execute_success(sql_id):
    if (settings.EMAIL_SEND_ENABLE):
        sql_info = get_sql_info_by_id(sql_id)
        sql_info.status_str = settings.SQL_WORK_STATUS_DICT[sql_info.status]
        sql_info.host_url = request.host_url
        if (len(sql_info.email) > 0):
            subject = "SQL工单-[{0}]-执行完成".format(sql_info.title)
            sql_info.work_url = "{0}sql/work/{1}".format(request.host_url, sql_info.id)
            content = render_template("mail_template.html", sql_info=sql_info)
            common_util.send_html(subject, sql_info.email, content)


# 开发人员获取工单方法
# 只能看到自己创建的工单
def get_sql_work_for_dev(obj):
    return get_sql_work_list_by_where(obj, "and create_user_id = {0}".format(obj.current_user_id))


# leader工单查询方法
# 能够看到自己的以及组内所以组员工单
def get_sql_work_for_leader(obj):
    sql_where = ""
    user_info = cache.MyCache().get_user_info(obj.current_user_id)
    if (obj.tab_type == settings.ALL_SQL_WORK_TAB):
        sql_where = " and create_user_id = {0}".format(obj.current_user_id)
    else:
        sql_where = " and (create_user_id = {0} or create_user_group_id = {1})".format(obj.current_user_id, user_info.group_id)
    return get_sql_work_list_by_where(obj, sql_where)


# dba工单查询方法
# 未执行工单可以看到自己的工单
# 以及别人指定执行的工单并且审核通过
def get_sql_work_for_dba(obj):
    sql_where = ""
    if (obj.tab_type == settings.ALL_SQL_WORK_TAB):
        sql_where = "and create_user_id = {0}".format(obj.current_user_id)
    elif (obj.tab_type == settings.NOT_EXECUTE_SQL_WORK_TAB):
        sql_where = " and (execute_user_id = {0} or create_user_id = {0})".format(obj.current_user_id)
    elif (obj.tab_type == settings.AUDIT_OK_SQL_WORK_TAB):
        sql_where = " and audit_user_id = {0}".format(obj.current_user_id)
    return get_sql_work_list_by_where(obj, sql_where)


# 合并方法，提取公共sql，精简代码
# 获取工单列表，根据where条件进行查询
def get_sql_work_list_by_where(obj, sql_where):
    if (obj.tab_type == settings.NOT_AUDIT_SQL_WORK_TAB):
        sql_where += " and status = {0}".format(settings.SQL_NO_AUDIT)
    elif (obj.tab_type == settings.AUDIT_OK_SQL_WORK_TAB):
        sql_where += " and status = {0}".format(settings.SQL_AUDIT_OK)
    elif (obj.tab_type == settings.AUDIT_FAIL_SQL_WORK_TAB):
        sql_where += " and status = {0}".format(settings.SQL_AUDIT_FAIL)
    elif (obj.tab_type == settings.NOT_EXECUTE_SQL_WORK_TAB):
        sql_where += " and status = {0}".format(settings.SQL_AUDIT_OK)
    elif (obj.tab_type == settings.EXECUTE_OK_SQL_WROK_TAB):
        sql_where += " and status = {0}".format(settings.SQL_EXECUTE_SUCCESS)
    elif (obj.tab_type == settings.EXECUTE_FAIL_SQL_WROK_TAB):
        sql_where += " and status = {0}".format(settings.SQL_EXECUTE_FAIL)

    sql = """select t1.*, t2.host_name
             from
             (
                 select id, title, create_user_id, audit_user_id, execute_user_id, audit_date_time,
                        execute_date_time, mysql_host_id, is_backup, execute_db_name,
                        backup_table, status, is_deleted, created_time, execute_finish_date_time,
                        create_user_name, audit_user_name, execute_user_name, real_execute_user_name
                 from mysql_audit.sql_work
                 where is_deleted = 0 {0} order by id desc limit {1}, {2}
             ) t1
             left join mysql_audit.mysql_hosts t2 on t1.mysql_host_id = t2.host_id"""
    sql = sql.format(sql_where, (obj.page_number - 1) * settings.SQL_LIST_PAGE_SIZE, settings.SQL_LIST_PAGE_SIZE)
    result_list = db_util.DBUtil().get_list_infos(settings.MySQL_HOST, sql)
    for info in result_list:
        get_sql_work_status_name(info)
    return result_list




