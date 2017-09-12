# SQL规范

## 建表规范
1. 使用Innodb引擎，MyISAM不要在使用
2. 为每个表设置一个自增的主键，如：id int unsigned not null primary key auto_increment
3. 选用合适的字段类型
> 1. 整型