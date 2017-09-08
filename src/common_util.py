# -*- coding: utf-8 -*-

import settings
from custom_entity import Entity

from email.mime.text import MIMEText
import smtplib, traceback, threadpool

threadpool_cache = threadpool.ThreadPool(settings.THREAD_POOL_SIZE)


# 把数据行转化为对象
def get_object(row):
    info = Entity()
    for key, value in row.items():
        if (value == "None"):
            value = None
        setattr(info, key, value)
    return info


# 发生文本邮件
def send_text(subject, to_list, content):
    send_mail(subject, to_list, content, "plain")


# 发送html邮件
def send_html(subject, to_list, content):
    send_mail(subject, to_list, content, "html")


# 发送邮件代码
def send_mail(subject, to_list, content, mail_type):
    list_t = []
    server = None
    if (isinstance(to_list, list) == False):
        list_t.append(to_list)
    try:
        message = MIMEText(content, _subtype=mail_type, _charset="utf8")
        message['Subject'] = subject
        message['To'] = ";".join(list_t)
        message['From'] = settings.EMAIL_USER

        server = smtplib.SMTP()
        server.connect(settings.EMAIL_HOST)
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_USER, list_t, message.as_string())
    except:
        traceback.print_exc()
    finally:
        if (server != None):
            server.close()


# 创建线程处理任务
def join_thread_pool(method_name, arg_list):
    requests = threadpool.makeRequests(method_name, arg_list, None)
    for request in requests:
        threadpool_cache.putRequest(request)
    threadpool_cache.poll()

