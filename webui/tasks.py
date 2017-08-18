#coding=utf-8
from celery import Task as T
from core.common import logger,Codis_admin_info
from api.models import *
import time

class BaseTask(T):
    error_info = None
    logger = logger

    def init(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

class Codis_info(BaseTask):

    def run(self,codis_id=None):
        codis=Codis.objects.get(id=codis_id)
        group_info=Codis_admin_info(codis.admin_http).group()
        for m in group_info:
            group_name="{0}{1}".format(codis.name,m.get('id'))
            Redis_group.objects.get_or_create(name=group_name)
            group=Redis_group.objects.get(name=group_name)
            group.slave.clear()
            group.offline.clear()
            for n in m.get('servers'):
                redis_instance=Redis_instance.objects.get_or_create(host=Ipv4Address.objects.get(name=n.get('addr').split()[0]),
                                                                    port=n.get('addr').split()[1]
                                                                    )
                if n.get('type').lower()=="master":
                    group.master=redis_instance
                    group.save()
                elif n.get('type').lower()=="slave":
                    group.salve.add(redis_instance)
                elif n.get('type').lower()=="offline":
                    group.offline.add(redis_instance)
                else:
                    pass

            codis.member.add(group)


# [
# {u'servers':
# [{u'group_id': 1, u'type': u'slave', u'addr': u'10.0.8.146:9939'},
# {u'group_id': 1, u'type': u'master', u'addr': u'10.0.8.144:9939'}],
# u'id': 1,
#  u'product_name':
#  u'codis_9939'},
# {u'servers':
# [{u'group_id': 2, u'type': u'master', u'addr': u'10.0.8.176:9939'},
# {u'group_id': 2, u'type': u'offline', u'addr': u'10.0.8.145:9939'}],
#  u'id': 2,
# u'product_name': u'codis_9939'}
# ]



class MissionTask(BaseTask):

    def run(self):
        for m in Codis.objects.all():
            if m.admin_http:
                Codis_info().apply_async(args=(m.id))