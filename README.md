# mysql_audit
轻量级的SQL审核和执行平台，支持回滚SQL功能</br>

# 未完成的功能
1. 目前还不支持pt-osc的执行
2. 权限功能不完善

# inception安装
安装还是看文档吧</br>
http://mysql-inception.github.io/inception-document/inception/</br>
```sql
-- 创建inception用户
grant all on *.* to yangcg@'%' identified by 'yangcaogui';
```

# 需要安装的python包
1. python2.7的环境
2. 调用inception只能使用MySQLdb
3. yum -y install python-devel python-setuptools
4. easy_install pip
5. pip install flask flask-login gevent threadpool pymysql DBUtils six packaging appdirs MySQLdb

# 导入表结构
mysql -h -u -p -P < table.sql</br>

# 修改配置文件
修改inception的服务地址：</br>
```python
inception_host = "192.168.11.101"
inception_port = 6669
inception_user = "yangcg"
inception_password = "yangcaogui"
```

修改MySQL数据库的地址：</br>
```python
MySQL_HOST = common_util.Entity()
MySQL_HOST.key = 99999
MySQL_HOST.host = "192.168.11.101"
MySQL_HOST.port = 3306
MySQL_HOST.user = "yangcg"
MySQL_HOST.password = "yangcaogui"
```

# 启动mysql_audit
python mysql_audit.py runserver</br>

# 后台启动
nohup python mysql_audit.py runserver &</br>

# 访问web服务
http://192.168.1.101:5200/login</br>
超级管理员登录：</br>
* 用户名：admin
* 密码：yang123!.+

# 备份注意点
1. 表必须有主键
2. 必须开启binlog日志
3. binlog_row_image必须为FULL
4. 必须使用参数--enable-remote-backup才能备份

# 联系方式
1. QQ：779647966
2. Email：ycg166911@163.com

# 界面展示
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/1.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/2.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/3.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/4.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/5.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/6.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/7.png)

