# -*- coding: utf-8 -*-

import db_util, settings, cache


# 添加用户并刷新缓存
def add_user(obj):
    if (obj.group_id <= 0):
        return "请选择用户组!"
    elif (obj.role_id <= 0):
        return "请选择用户角色!"
    elif (len(str(obj.email)) <= 0):
        return "请输入用户邮箱!"
    elif (len(str(obj.user_name)) <= 0):
        return "请输入用户名!"
    elif (len(str(obj.user_password)) <= 0):
        return "请输入密码!"
    elif (len(str(obj.chinese_name)) <= 0):
        return "请输入中文名!"

    sql = """insert into mysql_audit.work_user(user_name, user_password, chinese_name, group_id, role_id, email)
             VALUES
             ('{0}', md5('{1}'), '{2}', {3}, {4}, '{5}');
             update mysql_audit.group_info set user_count = user_count + 1 where group_id = {6};""" \
             .format(obj.user_name, obj.user_password, obj.chinese_name, obj.group_id, obj.role_id, obj.email, obj.group_id)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    cache.MyCache().load_user_infos()
    cache.MyCache().load_group_infos()
    return "添加用户成功!"


# 禁用用户
def delete_user(obj):
    sql = """update mysql_audit.work_user set is_deleted = 1 where user_id = {0};
             update mysql_audit.group_info set user_count = user_count - 1 where group_id = {6};""" .format(obj.user_id)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    cache.MyCache().load_all_cache()


# 启用用户
def start_user(obj):
    sql = """update mysql_audit.work_user set is_deleted = 0 where user_id = {0};
             update mysql_audit.group_info set user_count = user_count + 1 where group_id = {6};""" .format(obj.user_id)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    cache.MyCache().load_all_cache()


# 查询用户信息
def query_user(obj):
    where_sql = " 1=1 "
    if (obj.role_id > 0):
        where_sql += " and t1.role_id = {0}".format(obj.role_id)
    elif (obj.group_id > 0):
        where_sql += " and t1.group_id = {0}".format(obj.group_id)
    elif (len(str(obj.user_name)) > 0):
        where_sql += " and t1.user_name like '%{0}%'".format(obj.user_name)

    sql = """select t1.user_id, t1.user_name, t1.chinese_name, t1.created_time,
                    t1.email, ifnull(t2.role_name, '') as role_name, ifnull(t3.group_name, '') as group_name, t1.is_deleted
             from mysql_audit.work_user t1
             left join mysql_audit.role_info t2 on t1.role_id = t2.role_id
             left join mysql_audit.group_info t3 on t1.group_id = t3.group_id WHERE {0};""".format(where_sql)
    return db_util.DBUtil().get_list_infos(settings.MySQL_HOST, sql)


# 获取用户组信息
def get_user_group_infos():
    return db_util.DBUtil().get_list_infos(settings.MySQL_HOST, "select * from mysql_audit.group_info where is_deleted = 0;")


# 添加用户组信息
def add_group_info(obj):
    sql = "insert into mysql_audit.group_info (group_name, remark) VALUES ('{0}', '{1}');".format(obj.group_name, obj.remark)
    db_util.DBUtil().execute(settings.MySQL_HOST, sql)
    cache.MyCache().load_group_infos()
    return "添加用户组成功!"


# 更新用户组信息
def update_user_group_info(group_id):
    pass


# 删除用户组信息
def delete_user_group_info(group_id):
    pass

