#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from abstract.models import CommonModel,UniqueNameDescModel,NGINX_BASE,REDIS_BASE

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


class Docker_app(CommonModel, NGINX_BASE):
    host = models.ForeignKey(Ipv4Address)
    port = models.CharField(max_length=10)

    def __unicode__(self):
        return "{0}:{1}".format(self.host.name, self.port)
    @staticmethod
    def verbose():
        return u'Docker'

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
    direct_status=models.BooleanField(default=False)
    hosts=models.ManyToManyField(Ipv4Address,blank=True,related_name='upstream_host')
    port=models.CharField(max_length=20,blank=True)
    docker_list=models.ManyToManyField(Docker_app,blank=True,related_name='docker_app')
    status=models.ForeignKey(Status)
    ip_hash=models.BooleanField(default=False)

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
        if self.https:
            return "https://{0}".format(self.name)
        else:
            return "http://{0}".format(self.name)
    @staticmethod
    def verbose():
        return u'server_name'

class Site_context(CommonModel,NGINX_BASE):
    site=models.ForeignKey(Site)
    context=models.CharField(max_length=200)
    upstream=models.ForeignKey(Upstream,related_name='context_upstream')
    default_proxy_set=models.BooleanField(default=True)
    extra_parametres=models.TextField(blank=True)
    lua_status=models.BooleanField(default=True)
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


class Redis_instance(CommonModel,REDIS_BASE):
    host=models.ForeignKey(Ipv4Address,related_name='redis_host')
    port=models.CharField(max_length=5)
    version=models.CharField(blank=True,max_length=10)
    def __unicode__(self):
        return "{0}:{1}".format(self.host.name,self.port)

    @staticmethod
    def verbose():
        return u'Redis实例'

class Redis_group(CommonModel,REDIS_BASE):
    name=models.CharField(max_length=100)
    master=models.ForeignKey(Redis_instance,related_name='group_master',blank=True,null=True)
    slave=models.ManyToManyField(Redis_instance,related_name='group_slave',blank=True)
    offline=models.ManyToManyField(Redis_instance,related_name='group_offline',blank=True)

    def __unicode__(self):
        return self.name
    @staticmethod
    def verbose():
        return u'Redis组'

class Codis(CommonModel,REDIS_BASE):
    name=models.CharField(max_length=25,db_index=True)
    admin_http=models.URLField(blank=True)
    member=models.ManyToManyField(Redis_group,related_name='codis_group',blank=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def verbose():
        return u'Codis'

class Sentinel(CommonModel, REDIS_BASE):
    name = models.CharField(max_length=100)
    # from_host = models.CharField(max_length=25)
    member = models.ManyToManyField(Redis_group, related_name='sentinel_group', blank=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def verbose():
        return u'Sentinel'

class Redis_task(CommonModel,REDIS_BASE):
    master_ip=models.ForeignKey(Ipv4Address,blank=True,related_name='redis_master_ip',null=True)
    master_port=models.CharField(max_length=10,blank=True,null=True)
    redis_ip=models.ForeignKey(Ipv4Address,related_name='redis_instance_ip')
    redis_port=models.CharField(max_length=10)
    size=models.CharField(max_length=10)
    result=models.TextField(blank=True)
    status=models.ForeignKey(Status)

    @staticmethod
    def verbose():
        return u'Redis-Task'
    class Meta:
        ordering = ['-created_date', ]