CREATE DATABASE mysql_audit;

use mysql_audit;

CREATE TABLE work_user
(
  user_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(20) NOT NULL COMMENT '用户名',
  user_password VARCHAR(50) NOT NULL COMMENT '用户密码',
  chinese_name VARCHAR(10) NOT NULL DEFAULT '' COMMENT '用户中文名',
  group_id SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '属于哪个业务组，用于权限管理',
  role_id SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '角色id，用户权限管理',
  email varchar(30) NOT NULL DEFAULT '' COMMENT '用户邮件，用户发送消息给用户',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间',
  UNIQUE KEY userName (`user_name`)
) COMMENT '用户表' CHARSET utf8 ENGINE innodb;

insert into work_user (user_name, user_password, chinese_name, group_id, role_id,email) VALUES ("admin", md5("yang123!.+"), '超级管理员', 10002, 1001, 'ycg166911@163.com');

CREATE TABLE role_info
(
  role_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(30) NOT NULL COMMENT '角色名称',
  remark varchar(100) NOT NULL DEFAULT '' COMMENT '备注',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间'
) COMMENT '角色信息表例如：开发人员-组长-DBA' AUTO_INCREMENT=1003 CHARSET utf8 ENGINE innodb;

INSERT INTO role_info (role_id, role_name, remark) VALUES (1000, '组员', '开发人员只能查看自己创建的工具');
INSERT INTO role_info (role_id, role_name, remark) VALUES (1001, '组长', '开发组长能够查看本小组所有开发人员的历史数据');

CREATE TABLE group_info
(
  group_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  group_name VARCHAR(10) NOT NULL DEFAULT '' COMMENT '组名称',
  remark varchar(100) NOT NULL DEFAULT '' COMMENT '备注',
  user_count SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '组内用户数量',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间'
) COMMENT '用户组信息表' AUTO_INCREMENT=10003 CHARSET utf8 ENGINE innodb;

INSERT INTO group_info(group_id, group_name, remark) VALUES (10000, 'DBA组', '负责执行SQL的DBA小组');
INSERT INTO group_info(group_id, group_name, remark, user_count) VALUES (10002, '管理员组', '超级管理员权限', 1);

CREATE TABLE sql_work
(
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(100) NOT NULL COMMENT '标题，此sql对应的是什么业务',
  create_user_id SMALLINT UNSIGNED NOT NULL COMMENT '创建sql工单用户id',
  create_user_group_id SMALLINT UNSIGNED NOT NULL COMMENT '创建sql工单用户组id',
  audit_user_id SMALLINT UNSIGNED NOT NULL COMMENT '审核用户id',
  execute_user_id SMALLINT UNSIGNED NOT NULL COMMENT '创建工单的时候指定执行用户id',
  real_execute_user_id SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '真实执行SQL的用户id，一般和execute_user_id的值是一样的',
  create_user_name VARCHAR(20) NOT NULL DEFAULT '' COMMENT '创建sql工单用户名冗余字段',
  audit_user_name VARCHAR(20) NOT NULL DEFAULT '' COMMENT '审核用户名冗余字段',
  execute_user_name VARCHAR(20) NOT NULL DEFAULT '' COMMENT '执行用户名冗余字段',
  real_execute_user_name VARCHAR(20) NOT NULL DEFAULT '' COMMENT '真正执行sql的用户名称，冗余字段',
  audit_date_time DATETIME DEFAULT NULL COMMENT 'sql审核时间',
  execute_date_time DATETIME DEFAULT NULL COMMENT 'sql执行时间',
  execute_start_date_time DATETIME DEFAULT NULL COMMENT 'sql执行开始时间',
  execute_finish_date_time DATETIME DEFAULT NULL COMMENT 'sql执行完成时间',
  mysql_host_id SMALLINT UNSIGNED NOT NULL COMMENT '要执行的数据主机id',
  execute_db_name VARCHAR(50) NOT NULL DEFAULT 0 COMMENT '要执行的库名，如果不选，就需要在sql上使用use db',
  jira_url VARCHAR(100) NOT NULL DEFAULT '' COMMENT '对应的jira地址',
  is_backup TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '是否要备份，默认是备份',
  backup_table VARCHAR(50) NOT NULL DEFAULT '' COMMENT '备份之后的表名称',
  is_use_pt_osc TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否使用了pt-osc，默认没有使用',
  sleep FLOAT UNSIGNED NOT NULL DEFAULT 0 COMMENT '每条语句执行之后暂停多少毫秒，最小值0，最大值100秒，inception单位是毫秒，这边存储的是秒',
  sql_value MEDIUMTEXT COMMENT '要执行的sql内容',
  rollback_sql MEDIUMTEXT COMMENT '要回滚的SQL',
  audit_result_value MEDIUMTEXT COMMENT '审核的内容',
  return_value MEDIUMTEXT COMMENT '执行SQL返回的结果值',
  `status` TINYINT UNSIGNED NOT NULL COMMENT '状态 0：未审核 1：已审核 2：审核不通过 3：执行错误 4：执行成功 5：执行中 6：工单已撤销 7：工单已回滚',
  ignore_warnings TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0：不忽略警告 | 1：忽略警告',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间',
  KEY idx_create_user_id(`create_user_id`)
) COMMENT 'sql执行工单表' CHARSET utf8 ENGINE innodb;

#准备把上面的表进行拆分
#不过目前先不动，把功能先做好
CREATE TABLE sql_work_sub
(
  id INT UNSIGNED NOT NULL PRIMARY KEY,
  sql_value TEXT COMMENT '要执行的sql内容',
  audit_result_value TEXT COMMENT '审核的结果',
  execute_result_value TEXT COMMENT '执行的结果'
) COMMENT 'sql执行工单子表' CHARSET utf8 ENGINE innodb;

CREATE TABLE mysql_hosts
(
  host_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ip VARCHAR(20) NOT NULL COMMENT 'ip地址',
  port SMALLINT UNSIGNED NOT NULL DEFAULT 3306 COMMENT '端口',
  user VARCHAR(50) NOT NULL COMMENT '用户名',
  password VARCHAR(50) NOT NULL COMMENT '密码',
  is_test_host TINYINT NOT NULL DEFAULT 0 COMMENT '是否是测试实例',
  is_online_host TINYINT NOT NULL DEFAULT 0 COMMENT '是否是线上实例',
  host_name VARCHAR(20) NOT NULL DEFAULT '' COMMENT '主机名称，界面都是以这个内容显示',
  remark VARCHAR(50) NOT NULL DEFAULT '' COMMENT '备注',
  is_alive TINYINT NOT NULL DEFAULT 0 COMMENT '当前host是否连接正常',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间',
  UNIQUE KEY ip_port(`ip`, `port`) COMMENT '添加唯一键限制'
) COMMENT 'mysql主机地址信息表' CHARSET utf8 ENGINE innodb;


create table user_host_priv
(
  id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id SMALLINT UNSIGNED NOT NULL COMMENT '用户id',
  host_id SMALLINT UNSIGNED NOT NULL COMMENT '数据库主机id',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0,
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间'
) COMMENT '用户和数据库主机权限配置' CHARSET utf8 ENGINE innodb;
