#coding=utf-8
from celery import Task as T
from core.common import logger,Codis_admin_info,ANSRunner
from api.models import *
import redis
import time

class BaseTask(T):
    error_info = None
    logger = logger

    def init(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

class Codis_info(BaseTask):

    def _get_instance(self,host,port):
        redis_instance,redis_instance_status=Redis_instance.objects.get_or_create(
            host=Ipv4Address.objects.get(name=host),
            port=port
        )
        return redis_instance

    def _get_group(self,name):
        redis_group,redis_group_status=Redis_group.objects.get_or_create(name=name)
        return redis_group

    def _get_sentinel(self,name):
        sentinel,sentinel_status=Sentinel.objects.get_or_create(name=name)
        return sentinel

    def run(self,codis_id=None):
        codis=Codis.objects.get(id=codis_id)
        group_info=Codis_admin_info(codis.admin_http).group()
        for m in group_info:
            group_name="{0}_{1}".format(codis.name,m.get('id'))
            group,group_status=Redis_group.objects.get_or_create(name=group_name)
            if group_status:
                logger.info("{0} add to {1}".format(group_name,codis.name))
            group.slave.clear()
            group.offline.clear()
            for n in m.get('servers'):
                redis_instance,redis_instance_status=Redis_instance.objects.get_or_create(host=Ipv4Address.objects.get(name=n.get('addr').split(':')[0]),
                                                                    port=n.get('addr').split(':')[1]
                                                                    )
                if redis_instance_status:
                    logger.info("{0}:{1} add to {2}".format(redis_instance.host.name,redis_instance.port, group_name))
                if n.get('type').lower()=="master":
                    group.master=redis_instance
                    group.save()
                elif n.get('type').lower()=="slave":
                    group.slave.add(redis_instance)
                elif n.get('type').lower()=="offline":
                    group.offline.add(redis_instance)
                else:
                    pass

            codis.member.add(group)

class Sentinel_info(BaseTask):

    def _get_instance(self,host,port):
        redis_instance,redis_instance_status=Redis_instance.objects.get_or_create(
            host=Ipv4Address.objects.get(name=host),
            port=port
        )
        return redis_instance

    def _get_group(self,name):
        redis_group,redis_group_status=Redis_group.objects.get_or_create(name=name)
        return redis_group

    def _get_sentinel(self,name):
        sentinel,sentinel_status=Sentinel.objects.get_or_create(name=name)
        return sentinel

    def _get_slave(self,host,port,db):
        master=redis.Redis(host=host, port=port, db=db)
        master_info=master.info()
        slave_info=[master_info.get(x) for x in master_info.keys() if x.startswith('slave')]
        slaves=[]
        for n in slave_info:
            if isinstance(n,dict):
                slaves.append(n)
            elif isinstance(n,str):
                n_slave_str_line=n.split(',')
                slaves.append({"ip":n_slave_str_line[0],"port":n_slave_str_line[1],"state":n_slave_str_line[2]})
            else:
                logger.error("{0} not support this type {1}".format(n,type(n)))
        # slaves=[master_info.get(x).split(',') for x in master_info.keys() if x.startswith('slave')]
        slave_group=[]
        for m in [x for x in slaves if x.get('state')=='online']:
        # for m in slaves:
            m_redis_instance=self._get_instance(host=m.get('ip'),port=m.get('port'))
            slave_group.append(m_redis_instance)
        return slave_group



    def run(self, host,port,db):
        sentinel = redis.Redis(host=host, port=port, db=db)
        sentinel_info = sentinel.info()
        sentinel_group = [sentinel_info.get(x) for x in sentinel_info.keys() if x.startswith('master')]
        all_sentinel = {}

        sentinel_group_name = ['_'.join(x.get('name').split('_')[:-1]) for x in sentinel_group]
        for m in list(set(sentinel_group_name)):
            m_group = []
            for n in sentinel_group:
                if m == '_'.join(n.get('name').split('_')[:-1]):
                    m_group.append(n)
            all_sentinel[m]=m_group

        for k in all_sentinel.keys():
            m_sentinel=self._get_sentinel(name=k)
            m_sentinel.member.clear()
            for p in all_sentinel.get(k):
                m_sentinel_group=self._get_group(name=p.get('name'))
                m_sentinel.member.add(m_sentinel_group)
                m_host=p.get('address').split(':')[0]
                m_port=p.get('address').split(':')[1]
                m_sentinel_group.master=self._get_instance(
                    host=m_host,
                    port=m_port
                )
                m_sentinel_group.save()
                m_sentinel_group.slave.clear()
                slaves=self._get_slave(m_host,m_port,0)
                for n in slaves:
                    m_sentinel_group.slave.add(n)

class MissionTask(BaseTask):

    def run(self):
        for m in Codis.objects.all():
            if m.admin_http:
                Codis_info().apply_async(args=(m.id,))



class Run_ansible_redis_task(BaseTask):


    def run(self,redis_task_id):
        task=Redis_task.objects.get(id=redis_task_id)
        if task.status.name=='in_queue':
            task.status=Status.objects.get(name='processing')
            task.save()
            resource = [{"hostname": task.redis_ip.name,"username": "root", "ssh_key":"/root/.ssh/id_rsa"}]
            if task.master_ip:
                playbook_path = '/home/admin/scripts/redis_shihui/slave.yml'
                parametres={
                    "host":[task.redis_ip.name],
                    "master_ip":task.master_ip.name,
                    "master_port":task.master_port,
                    "ip":task.redis_ip.name,
                    "port":task.redis_port,
                    "maxmemory":task.size
                }
            else:
                playbook_path='/home/admin/scripts/redis_shihui/master.yml'
                parametres = {
                    "host": [task.redis_ip.name],
                    "ip": task.redis_ip.name,
                    "port": task.redis_port,
                    "maxmemory": task.size
                }
            rbt = ANSRunner(resource)
            rbt.run_playbook(
                playbook_path=playbook_path,
                extra_vars=parametres
            )
            result_data = rbt.get_playbook_result()
            logger.info({"resource":resource,"result":result_data,"exec_id":redis_task_id})
            publish_status=True
            if result_data.get('failed'):
                publish_status=False
            if result_data.get('skipped'):
                publish_status = False
            if result_data.get('unreachable'):
                publish_status = False

            if publish_status:
                task.status=Status.objects.get(name='done')
                task.result='done'
                task.save()
            else:
                logger.error(result_data)
                task.status.status=Status.objects.get(name='failed')
                task.status.result=result_data
                task.save()
        else:
            logger.error("{0} wrong status".format(redis_task_id))