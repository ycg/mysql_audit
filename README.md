# mysql_audit
轻量级的SQL审核和执行平台，支持回滚SQL功能</br>
</br>
</br>

# 未完成的功能
目前还不支持pt-osc的执行</br>
还不支持查看pt-osc执行的进度</br>

# 需要安装的python包
python2.7的环境</br>
pip install flask flask-login gevent threadpool pymysql DBUtils six packaging appdirs</br>

# 修改配置文件
修改inception的服务地址：</br>
`
inception_host = "192.168.11.101"
inception_port = 6669
inception_user = "yangcg"
inception_password = "yangcaogui"
`

修改MySQL数据库的地址：</br>
`
MySQL_HOST = common_util.Entity()
MySQL_HOST.key = 99999
MySQL_HOST.host = "192.168.11.101"
MySQL_HOST.port = 3306
MySQL_HOST.user = "yangcg"
MySQL_HOST.password = "yangcaogui"
`

# 启动mysql_audit
python mysql_audit.py runserver</br>
</br>
</br>

![image](https://github.com/ycg/mysql_audit/blob/master/static/img/1.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/2.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/3.png)
![image](https://github.com/ycg/mysql_audit/blob/master/static/img/4.png)

