# -*- coding: utf-8 -*-

import settings
import MySQLdb, sys

reload(sys)
sys.setdefaultencoding("utf8")

class MyEntity():
    def __init__(self):
        pass

host_info = MyEntity()
host_info.host = "192.168.11.101"
host_info.port = 3306
host_info.user = "yangcg"
host_info.password = "yangcaogui"

sql_audit_flag = "--enable-check;"
sql_execute_flag = "--enable-execute;"

sql_mode = """/*--host={0};--port={1};--user={2};--password={3};{4}*/
              inception_magic_start;
              {5}
              inception_magic_commit;"""

result_fields = ['ID', 'stage', 'errlevel', 'stagestatus', 'errormessage', 'SQL', 'Affected_rows', 'sequence', 'backup_dbname', 'execute_time', 'sqlsha1']

def sql_audit(sql, host_info):
    sql = sql_mode.format(host_info.host, host_info.port, host_info.user, host_info.password, sql_audit_flag, sql)
    return get_result_infos(execute_sql(sql))

def sql_execute(sql, host_info):
    sql = sql_mode.format(host_info.host, host_info.port, host_info.user, host_info.password, sql_execute_flag, sql)
    return get_result_infos(execute_sql(sql))

def stop_osc_task(sha1_code):
    sql = "inception stop alter '{}'".format(sha1_code)
    return execute_sql(sql)

def get_osc_info(sha1_code):
    sql = "inception get osc_percent '{0}'".format(sha1_code)
    return execute_sql(sql)

def get_result_infos(rows):
    result = []
    for row in rows:
        info = MyEntity()
        for i in range(0, len(result_fields)):
            setattr(info, result_fields[i], row[i])
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

my_sql = """use mysql_web;
CREATE TABLE backup_task
(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  host_id MEDIUMINT NOT NULL,
  backup_name VARCHAR(30) NOT NULL,
  backup_tool TINYINT NOT NULL,
  backup_mode TINYINT NOT NULL,
  backup_cycle VARCHAR(30) NOT NULL,
  backup_time TIME NOT NULL,
  backup_save_days MEDIUMINT UNSIGNED NOT NULL,
  backup_compress TINYINT UNSIGNED NOT NULL,
  backup_upload_host TINYINT UNSIGNED NOT NULL,
  created_time TIMESTAMP NOT NULL DEFAULT now(),
  updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  aa varchar(100) not null default '你好啊'
);"""

#my_sql = "select * from mysql_web.host_infos where host_id = 1;"

cc = sql_audit(my_sql, host_info)
for dd in cc:
    print(dd.errormessage)

get_osc_info("dsadsadsadsa")