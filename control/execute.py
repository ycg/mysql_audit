from common import cache

def get_execute_mysql_host():
    return cache.MyCache().get_mysql_host_info()
