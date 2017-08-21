import db_util, settings, common_util, custom_algorithm

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
            info = common_util.get_object(row)
            info.user = custom_algorithm.decrypt(settings.MY_KEY, info.user)
            info.password = custom_algorithm.decrypt(settings.MY_KEY, info.password)
            self.__user_infos[row["user_id"]] = info

    def load_role_infos(self):
        rows = db_util.DBUtil().fetchall(settings.MySQL_HOST, "select * from mysql_audit.role_info")
        self.__role_infos.clear()
        for row in rows:
            self.__role_infos[row["role_id"]] = common_util.get_object(row)

    def load_group_infos(self):
        rows = db_util.DBUtil().fetchall(settings.MySQL_HOST, "select * from mysql_audit.group_info")
        self.__group_infos.clear()
        for row in rows:
            self.__group_infos[row["group_id"]] = common_util.get_object(row)

    def load_mysql_host_infos(self):
        rows = db_util.DBUtil().fetchall(settings.MySQL_HOST, "select * from mysql_audit.mysql_hosts WHERE is_deleted = 0;")
        self.__mysql_host_infos.clear()
        for row in rows:
            info = common_util.get_object(row)
            info.host = info.ip
            info.key = info.host_id
            self.__mysql_host_infos[row["host_id"]] = info

    def get_value_by_key(self, dic, key=None):
        if(key in dic.keys()):
            return dic[key]
        return dic.values()

    def get_user_info(self, user_id=None):
        return self.get_value_by_key(self.__user_infos, user_id)

    def get_user_info_by_role(self, role_id):
        user_list = []
        for info in self.__user_infos.values():
            if(info.role_id == role_id):
                user_list.append(info)
        return user_list

    def get_role_info(self, role_id=None):
        return self.get_value_by_key(self.__role_infos, role_id)

    def get_group_info(self, group_id=None):
        return self.get_value_by_key(self.__group_infos, group_id)

    def get_mysql_host_info(self, host_id=None):
        return self.get_value_by_key(self.__mysql_host_infos, host_id)
