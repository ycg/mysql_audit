import settings
from common import cache, db_util

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

