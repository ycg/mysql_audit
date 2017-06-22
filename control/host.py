
from common import cache

def query_host_infos(parameter):
    result = cache.MyCache().get_mysql_host_info(host_id=parameter.host_id)

    if(parameter.host_type > 0):
        pass
    if(len(parameter.host_name) > 0):
        pass
    return result

def query(list_tmp):
    result = []

    for info in list_tmp:
        pass

    map()

