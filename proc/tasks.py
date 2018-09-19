#coding=utf-8
from celery import Task as T
from core.common import logger,Codis_admin_info,ANSRunner
from .models import Machine_procs,History_procs
import redis
import datetime
class BaseTask(T):
    error_info = None
    logger = logger

    def init(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

class Proc_info(BaseTask):
    def _get_proc(self,host,proc_info):
        pid=proc_info.get('pid')
        name=proc_info.get('name')
        username=proc_info.get('username')
        start_time=datetime.datetime.fromtimestamp(proc_info.get('start_time'))
        if Machine_procs.objects.filter(
            host=host,
            pid=pid,
            name=name,
            username=username
        ).count()==0:
            History_procs.objects.create(
                host=host,
                pid=pid,
                name=name,
                username=username,
                start_time=start_time,
                record='new'
            )
            Machine_procs.objects.create(
                host=host,
                pid=pid,
                name=name,
                username=username,
                start_time=start_time,
                status='online'
            )

    def _del_proc(self,proc):
        History_procs.objects.create(
            host=proc.host,
            pid=proc.pid,
            name=proc.name,
            username=proc.username,
            start_time=proc.start_time,
            record='delete'
        )
        proc.delete()

    def run(self, host,procs):
        Machine_procs.objects.filter(host=host,status='offline').delete()
        Machine_procs.objects.filter(host=host,status='online').update(status='standby')
        for m in procs:
            self._get_proc(host,m)
        for n in Machine_procs.objects.filter(host=host,status='standby'):
            self._del_proc(n)