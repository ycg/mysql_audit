from common import inception_util, entity

host_info = entity.Entity()
host_info.host = "192.168.11.101"
host_info.port = 3306
host_info.user = "yangcg"
host_info.password = "yangcaogui"

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
  aa varchar(100) not null
);"""

#my_sql = "select * from mysql_web.host_infos where host_id = 1;"
execute_fields = ['ID', 'stage', 'errlevel', 'stagestatus', 'errormessage', 'SQL', 'Affected_rows', 'sequence', 'backup_dbname', 'execute_time', 'sqlsha1']

cc = inception_util.sql_audit(my_sql, host_info)
for dd in cc:
    print(dd.id, dd.stage, dd.errlevel, dd.stagestatus, dd.errormessage, dd.sql)
    #print(dd.errormessage)

#inception_util.get_osc_info("dsadsadsadsa")

import control
from control import host
print(host.query_host_infos([]))