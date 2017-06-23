CREATE DATABASE mysql_audit;

CREATE TABLE work_user
(
  user_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(20) NOT NULL COMMENT '用户名',
  user_password VARCHAR(50) NOT NULL COMMENT '用户密码',
  chinese_name VARCHAR(10) NOT NULL DEFAULT '' COMMENT '用户中文名',
  group_id SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '属于哪个业务组，用于权限管理',
  role_id SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '角色id，用户权限管理',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间'
) COMMENT '用户表';

CREATE TABLE role_info
(
  role_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(10) NOT NULL COMMENT '角色名称',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间'
) COMMENT '角色信息表例如：开发人员-组长-DBA';

CREATE TABLE sql_work
(
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  create_user_id SMALLINT UNSIGNED NOT NULL COMMENT '创建sql工单用户id',
  audit_user_id SMALLINT UNSIGNED NOT NULL COMMENT '审核用户id',
  execute_user_id SMALLINT UNSIGNED NOT NULL COMMENT '执行用户id',
  audit_date_time DATETIME COMMENT 'sql审核时间',
  execute_date_time DATETIME COMMENT 'sql执行时间',
  mysql_host_id SMALLINT UNSIGNED NOT NULL COMMENT '要执行的数据主机id',
  jira_url VARCHAR(100) NOT NULL DEFAULT '' COMMENT '对应的jira地址',
  is_backup TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '是否要备份，默认是备份',
  backup_table VARCHAR(50) NOT NULL DEFAULT '' COMMENT '备份之后的表名称',
  sql_value TEXT COMMENT '要执行的sql内容',
  return_value TEXT COMMENT '返回的结果值',
  status TINYINT UNSIGNED NOT NULL COMMENT '状态',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间'
) COMMENT 'sql执行工单表';

CREATE TABLE mysql_hosts
(
  host_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ip VARCHAR(20) NOT NULL COMMENT 'ip地址',
  port SMALLINT UNSIGNED NOT NULL DEFAULT 3306 COMMENT '端口',
  user VARCHAR(20) NOT NULL COMMENT '用户名',
  password VARCHAR(50) NOT NULL COMMENT '密码',
  is_test_host TINYINT NOT NULL DEFAULT 0 COMMENT '是否是测试实例',
  is_online_host TINYINT NOT NULL DEFAULT 0 COMMENT '是否是线上实例',
  host_name VARCHAR(20) NOT NULL DEFAULT '' COMMENT '主机名称，界面都是以这个内容显示',
  remark VARCHAR(50) NOT NULL DEFAULT '' COMMENT '备注',
  is_deleted TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否被删除',
  created_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  updated_time DATETIME NOT NULL DEFAULT NOW() ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更改时间'
) COMMENT 'mysql主机地址信息表';

insert into mysql_hosts (ip,user,password,is_test_host,host_name,remark)values("192.168.11.101","yangcg","yangcaogui", 1, "jumpserver","jump server");