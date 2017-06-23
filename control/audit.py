# -*- coding: utf-8 -*-

from flask import render_template

from common import cache, inception_util

def audit_sql(obj):
    if(len(obj.sql) <= 0):
        return "请输入SQL"
    if(obj.host_id <= 0):
        return "请选择审核集群"
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(obj.sql, cache.MyCache().get_mysql_host_info(obj.host_id)))

def get_audit_mysql_host():
    return cache.MyCache().get_mysql_host_info()

