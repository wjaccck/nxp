#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from abstract.models import CommonModel,UniqueNameDescModel,ITEM_BASE,PUBLISH_BASE,NGINX_BASE

# from core.common import content
class Ipv4Address(UniqueNameDescModel):

    class Meta:
        ordering = ['name', ]

class Ipv4Network(UniqueNameDescModel):
    gateway = models.CharField(max_length=18, null=True)

    class Meta:
        ordering = ['name', ]


class Status(CommonModel,NGINX_BASE):
    name=models.CharField(max_length=50,unique=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def verbose():
        return u'状态'

class Group(CommonModel,NGINX_BASE):
    name=models.CharField(max_length=50,unique=True)
    hosts=models.ManyToManyField(Ipv4Address,related_name='group_host')

    def __unicode__(self):
        return self.name

    @staticmethod
    def verbose():
        return u'nginx组'

class Upstream(CommonModel,NGINX_BASE):
    name=models.CharField(max_length=50,unique=True)
    direct_status=models.BooleanField(blank=True)
    hosts=models.ManyToManyField(Ipv4Address,blank=True,related_name='upstream_host')
    port=models.CharField(max_length=20,blank=True)
    status=models.ForeignKey(Status)

    def __unicode__(self):
        return self.name

    @staticmethod
    def verbose():
        return u'upstream组'

class Site(CommonModel,NGINX_BASE):
    name=models.CharField(max_length=50)
    group=models.ForeignKey(Group,related_name='site_group')
    https=models.BooleanField()

    def __unicode__(self):
        return self.name
    @staticmethod
    def verbose():
        return u'server_name'

class Site_context(CommonModel,NGINX_BASE):
    site=models.ForeignKey(Site)
    context=models.CharField(max_length=200)
    upstream=models.ForeignKey(Upstream,related_name='context_upstream')
    extra_parametres=models.TextField(blank=True)
    status=models.ForeignKey(Status)
    @staticmethod
    def verbose():
        return u'context匹配详情'



class Nxp_mission(CommonModel,NGINX_BASE):
    mark=models.CharField(max_length=50,db_index=True)
    site=models.ForeignKey(Site)
    files=models.TextField()
    host=models.ForeignKey(Ipv4Address)
    status=models.ForeignKey(Status)
    remark=models.TextField(blank=True)
    @staticmethod
    def verbose():
        return u'更新过程'
