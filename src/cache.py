# -*- coding: utf-8 -*-

import db_util, settings, common_util, custom_algorithm, host_manager

class MyCache():
    __user_infos = {}
    __role_infos = {}
    __group_infos = {}
    __mysql_host_infos = {}

    def __init__(self):
        pass

    def load_all_cache(self):
        self.load_user_infos()
        self.load_role_infos()
        self.load_group_infos()
        self.load_mysql_host_infos()

    def load_user_infos(self):
        rows = db_util.DBUtil().fetchall(settings.MySQL_HOST, "select * from mysql_audit.work_user")
        self.__user_infos.clear()
        for row in rows:
            self.__user_infos[row["user_id"]] = common_util.get_object(row)

    def load_role_infos(self):
        rows = db_util.DBUtil().fetchall(settings.MySQL_HOST, "select * from mysql_audit.role_info")
        self.__role_infos.clear()
        for row in rows:
            self.__role_infos[row["role_id"]] = common_util.get_object(row)

    def load_group_infos(self):
        rows = db_util.DBUtil().fetchall(settings.MySQL_HOST, "select * from mysql_audit.group_info where is_deleted = 0;")
        self.__group_infos.clear()
        for row in rows:
            self.__group_infos[row["group_id"]] = common_util.get_object(row)

    def load_mysql_host_infos(self):
        rows = db_util.DBUtil().fetchall(settings.MySQL_HOST, "select * from mysql_audit.mysql_hosts WHERE is_deleted = 0;")
        for row in rows:
            info = common_util.get_object(row)
            if (info.host_id not in self.__mysql_host_infos.keys()):
                info.host = info.ip
                info.key = info.host_id
                info.user = custom_algorithm.decrypt(settings.MY_KEY, info.user)
                info.password = custom_algorithm.decrypt(settings.MY_KEY, info.password)
                info.host_ip = info.host
                info.host_port = info.port
                info.host_user = info.user
                info.host_password = info.password
                info.is_alive = host_manager.test_connection_new(info)
                self.__mysql_host_infos[info.host_id] = info

    def get_value_by_key(self, dic, key=None):
        if (key in dic.keys()):
            return dic[key]
        return dic.values()

    def get_user_info(self, user_id=None):
        return self.get_value_by_key(self.__user_infos, user_id)

    def get_user_info_by_role(self, role_id):
        user_list = []
        for info in self.__user_infos.values():
            if (info.role_id == role_id and info.is_deleted == 0):
                user_list.append(info)
        return user_list

    def get_user_email(self, user_id):
        return self.get_user_info(user_id).email

    def get_user_chinese_name(self, user_id):
        return self.get_user_info(user_id).chinese_name

    def get_audit_user_infos(self):
        # 获取审核用户信息，只显示组长，DBA用户
        audit_infos = []
        for user_info in self.__user_infos.values():
            if (user_info.role_id == settings.ROLE_LEADER or user_info.group_id == settings.DBA_GROUP_ID):
                audit_infos.append(user_info)
        return audit_infos

    def get_user_info_by_group_id(self, group_id):
        user_list = []
        for info in self.__user_infos.values():
            if (info.group_id == group_id and info.is_deleted == 0):
                user_list.append(info)
        return user_list

    def get_role_info(self, role_id=None):
        return self.get_value_by_key(self.__role_infos, role_id)

    def get_group_info(self, group_id=None):
        return self.get_value_by_key(self.__group_infos, group_id)

    def get_mysql_host_info(self, host_id=None):
        return self.get_value_by_key(self.__mysql_host_infos, host_id)

    def delete_host_info_by_host_id(self, host_id):
        if (host_id in self.__mysql_host_infos.keys()):
            self.__mysql_host_infos.pop(host_id)
