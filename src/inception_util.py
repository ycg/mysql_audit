# -*- coding: utf-8 -*-

import MySQLdb, sys
import settings, common_util

reload(sys)
sys.setdefaultencoding("utf8")

sql_audit_flag = "--enable-check;"
sql_execute_flag = "--enable-execute;"
sqL_enable_split_flag = "--enable-split"

sql_mode = """/*--host={0};--port={1};--user={2};--password={3};{4}*/
              inception_magic_start;
              {5}
              inception_magic_commit;"""

sql_mode_no_host = "inception_magic_start;{0}inception_magic_commit;"

osc_fields = ["DBNAME", "TABLENAME", "SQLSHA1", "PERCENT", "REMAINTIME", "INFORMATION"]
execute_fields = ['ID', 'stage', 'errlevel', 'stagestatus', 'errormessage', 'SQL', 'Affected_rows', 'sequence', 'backup_dbname', 'execute_time', 'sqlsha1']

def sql_audit(sql, host_info):
    sql = sql_mode.format(host_info.host, host_info.port, host_info.user, host_info.password, sql_audit_flag, sql)
    return get_object(execute_sql(sql), fields=execute_fields)

def sql_execute(sql, host_info):
    sql = sql_mode.format(host_info.host, host_info.port, host_info.user, host_info.password, sql_execute_flag, sql)
    return get_object(execute_sql(sql), fields=execute_fields)

def stop_osc_task(sha1_code):
    sql = "inception stop alter '{}';".format(sha1_code)
    return get_object(execute_sql(sql_mode_no_host.format(sql)), fields=osc_fields)

def get_osc_info(sha1_code):
    sql = "inception get osc_percent '{}';".format(sha1_code)
    return get_object(execute_sql(sql_mode_no_host.format(sql)), fields=osc_fields)

def get_object(rows, fields=None):
    result = []
    if(rows == None or len(rows) <= 0 or fields == None or len(fields) <= 0):
        return result
    for row in rows:
        info = common_util.Entity()
        for i in range(0, len(fields)):
            setattr(info, fields[i].lower(), row[i])
        result.append(info)
    return result

def execute_sql(sql):
    connection, cursor = None, None
    try:
        connection = MySQLdb.connect(host=settings.inception_host, user=settings.inception_user, passwd=settings.inception_password, port=settings.inception_port, use_unicode=True, charset="utf8")
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if(cursor != None):
            cursor.close()
        if(connection != None):
            connection.close()
    return []

