#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from abstract.models import CommonModel,UniqueNameDescModel,NGINX_BASE,REDIS_BASE
import time,datetime
# from core.common import content
class Machine_procs(CommonModel,NGINX_BASE):
    host=models.CharField(max_length=18,db_index=True)
    pid=models.IntegerField()
    name=models.CharField(max_length=200)
    username=models.CharField(max_length=50)
    start_time=models.DateTimeField()
    status=models.CharField(max_length=10)

    @staticmethod
    def verbose():
        return u'服务器进程信息'

class History_procs(CommonModel,NGINX_BASE):
    host=models.CharField(max_length=18,db_index=True)
    pid=models.IntegerField()
    name=models.CharField(max_length=200)
    username=models.CharField(max_length=50)
    start_time=models.DateTimeField()
    record=models.CharField(max_length=10)

    @staticmethod
    def verbose():
        return u'服务器进程变更记录'