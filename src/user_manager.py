import db_util, settings, common_util

def add_user():
    pass

def delete_user():
    pass

def query_user(obj):
    sql = """select t1.user_id, t1.user_name, t1.chinese_name, t1.email, ifnull(t2.role_name, '') as role_name, ifnull(t3.group_name, '') as group_name
             from mysql_audit.work_user t1
             left join mysql_audit.role_info t2 on t1.role_id = t2.role_id
             left join mysql_audit.group_info t3 on t1.group_id = t3.group_id;"""""
    return db_util.DBUtil().get_list_infos(settings.MySQL_HOST, sql)

