__author__ = 'jinhongjun'
import logging
logger = logging.getLogger("nxp")
from jinja2 import Template,Environment
import commands
import paramiko
import requests
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory, Host, Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor

pkey='/root/.ssh/id_rsa'
head_file="/opt/app/nxp/templates/nginx/head.conf"
shihui_https_file="/opt/app/nxp/templates/nginx/17shihui_https.conf"
vhost_j2="/opt/app/nxp/templates/nginx/vhost.j2"
upstream_j2="/opt/app/nxp/templates/nginx/upstream.j2"
hiwemeet_https_file="/opt/app/nxp/templates/nginx/hiwemeet_https.conf"
context_file="/opt/app/nxp/templates/nginx/context.conf"
redirect_file="/opt/app/nxp/templates/nginx/redirect.conf"
tail_file="/opt/app/nxp/templates/nginx/tail.conf"
upstream_file="/opt/app/nxp/templates/nginx/upstream.conf"
upstream_tmp_file="/opt/app/nxp/templates/conf/tmp/upstream/{0}.conf"
vhost_tmp_file="/opt/app/nxp/templates/conf/tmp/vhost.d/{0}.conf"
ssl_vhost_tmp_file="/opt/app/nxp/templates/conf/tmp/vhost.d/ssl.{0}.conf"
upstream_release_file="/opt/app/nxp/templates/conf/release/upstream/{0}.conf"
vhost_release_file="/opt/app/nxp/templates/conf/release/vhost.d/{0}.conf"
ssl_vhost_release_file="/opt/app/nxp/templates/conf/release/vhost.d/ssl.{0}.conf"
upstream_online_file="/opt/nginx/conf/upstream/{0}.conf"
vhost_online_file="/opt/nginx/conf/vhost.d/{0}.conf"
ssl_vhost_online_file="/opt/nginx/conf/vhost.d/ssl.{0}.conf"

###
sentinel_host=[{"host":"10.0.8.119","port":"26379","db":0}]

def generate_conf(source_file,target_file,info):
    try:
        with open(source_file, 'r') as in_file, open(target_file, 'w') as out_file:
            tmle = Template(in_file.read())
            out_file.write(tmle.render(info))
        return get_result(0,'{0} format {1} done'.format(source_file,target_file))
    except Exception as e:
        return get_result(1,'{0} format {1} failed the reason is {2}'.format(source_file,target_file,str(e)))



def get_file_content(file_path):
    with open(file_path, 'r') as f:
        content=f.read()

    return content


def get_result(status,content):
    if status==0:
        result={
                "retcode":0,
                "stdout":content,
                "stderr":''
                }
    else:
        result={
                "retcode":status,
                "stdout":'',
                "stderr":content
                }
    return result

def getComStr(cmd):
    try:
        stat, proStr = commands.getstatusoutput(cmd)
        return get_result(stat,proStr)
    except:
        logger.error('can not run {0} '.format(cmd))
        return get_result(1,'can not run {0} '.format(cmd))

class Cmd_ssh(object):
    key=None
    def __init__(self,host,user='admin',password='admin@eju',pkey=None):
        self.user=user
        self.password=password
        self.host=host
        self.pkey=pkey
        self.ssh=paramiko.SSHClient()

    def _close(self):
        return self.ssh.close()
    def _key_ssh(self,cmd):
        try:
            self.ssh = paramiko.SSHClient()
            self.key=paramiko.RSAKey.from_private_key_file(self.pkey)
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host,username = self.user,pkey=self.key)
            stdin,stdout,stderr=self.ssh.exec_command(cmd)
            channel = stdout.channel
            status = channel.recv_exit_status()
            if status==0:
                result = get_result(0, stdout.read().strip())
            else:
                result = get_result(1,stderr.read().strip())
            self.ssh.close()
            return result
        except Exception,e:
            return get_result(1,str(e))

    # def _passwd_ssh(self,cmd):
    #     try:
    #         self.ssh = paramiko.SSHClient()
    #         self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #         self.ssh.connect(self.host,username = self.user,password=self.password)
    #         stdin,stdout,stderr=self.ssh.exec_command(cmd)
    #         err_list = stderr.readlines()
    #
    #         if len(err_list) > 0:
    #             return get_result(1,'ERROR:' + err_list[0])
    #
    #         result=get_result(0,stdout.read().strip())
    #         self.ssh.close()
    #         return result
    #     except Exception,e:
    #         return get_result(1,str(e))

    def _upload(self,local_file,remote_file):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.load_system_host_keys()
            self.ssh.connect(self.host,username = self.user,pkey=self.key)
            sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
            sftp = self.ssh.open_sftp()
            sftp.put(local_file, remote_file)
            self.ssh.close()
            return get_result(0,'done')
        except Exception,e:
            return get_result(1,str(e))
    def run(self,cmd='id'):
        # if self.key:
        return self._key_ssh(cmd)
        # else:
        #     return self._passwd_ssh(cmd)
    def upload(self,local_file,remote_file):
        return self._upload(local_file,remote_file)



class Codis_admin_info(object):
    def __init__(self,admin_http):
        self.admin_http=admin_http
        self.header={"Content-Type": "application/json"}
    def _get(self,url):
        conn=requests.get(url,headers=self.header)
        return conn.json()
    def group(self):
        url="{0}/api/server_groups".format(self.admin_http)
        result=self._get(url)
        return result
    # def _check_redis(group_url):
    #     url="{0}/api/server_groups".format(group_url)
    #     result=get(url)
    #     print result
    #     for m in result:
    #         for n in m.get('servers'):
    #             check_url=None
    #             check_result=None
    #             check_url="{0}/api/redis/{1}/stat?group_id={2}&type={3}".format(group_url,n.get('addr'),n.get('group_id'),n.get('type'))
    #             check_result=get(check_url)
    #             print check_url
    #             print check_result
    #             print "{0}/{1}".format(check_result.get('used_memory'),check_result.get('maxmemory'))



class MyInventory(Inventory):
    """ 
    this is my ansible inventory object. 
    """

    def __init__(self, resource, loader, variable_manager):
        self.resource = resource
        self.inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[])
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        """ 
            add hosts to a group 
        """
        my_group = Group(name=groupname)

        # if group variables exists, add them to group
        if groupvars:
            for key, value in groupvars.iteritems():
                my_group.set_variable(key, value)

                # add hosts to group
        for host in hosts:
            # set connection variables
            hostname = host.get("hostname")
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key")
            my_host = Host(name=hostname, port=hostport)
            my_host.set_variable('ansible_ssh_host', hostip)
            my_host.set_variable('ansible_ssh_port', hostport)
            my_host.set_variable('ansible_ssh_user', username)
            my_host.set_variable('ansible_ssh_pass', password)
            my_host.set_variable('ansible_ssh_private_key_file', ssh_key)

            # set other variables
            for key, value in host.iteritems():
                if key not in ["hostname", "port", "username", "password"]:
                    my_host.set_variable(key, value)
                    # add to group
            my_group.add_host(my_host)

        self.inventory.add_group(my_group)

    def dynamic_inventory(self):
        """ 
            add hosts to inventory. 
        """
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.iteritems():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))

class ModelResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result

class PlayBookResultsCollector(CallbackBase):
    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }

class ANSRunner(object):
    """ 
    This is a General object for parallel execute modules. 
    """

    def __init__(self, resource, redisKey=None, logId=None, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}
        self.redisKey = redisKey
        self.logId = logId

    def __initializeData(self):
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                         'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity',
                                         'check', 'listhosts', 'listtasks', 'listtags', 'syntax'])

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                               remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False)

        self.passwords = dict(sshpass=None, becomepass=None)
        self.inventory = MyInventory(self.resource, self.loader, self.variable_manager).inventory
        self.variable_manager.set_inventory(self.inventory)

    def run_model(self, host_list, module_name, module_args):
        """ 
        run module from andible ad-hoc. 
        module_name: ansible module_name 
        module_args: ansible module args 
        """
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        self.callback = ModelResultsCollector()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
            )
            tqm._stdout_callback = self.callback
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, playbook_path, extra_vars=None):
        """ 
        run ansible palybook 
        """
        try:
            self.callback = PlayBookResultsCollector()
            if extra_vars: self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            executor.run()
        except Exception as e:
            return False

    def get_model_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result

        return json.dumps(self.results_raw)

    def get_playbook_result(self):
        self.results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}}

        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result._result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result._result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        return self.results_raw

# if __name__ == '__main__':
#     resource = [
#         {"hostname": "10.120.180.1"},
#         {"hostname": "10.120.180.2"},
#         {"hostname": "10.120.180.3"},
#     ]
#     #     resource =  {
#     #                     "dynamic_host": {
#     #                         "hosts": [
#     #                                     {"hostname": "192.168.1.34", "port": "22", "username": "root", "password": "jinzhuan2015"},
#     #                                     {"hostname": "192.168.1.130", "port": "22", "username": "root", "password": "jinzhuan2015"}
#     #                                   ],
#     #                         "vars": {
#     #                                  "var1":"ansible",
#     #                                  "var2":"saltstack"
#     #                                  }
#     #                     }
#     #                 }
#
#     rbt = ANSRunner(resource)
#     rbt.run_playbook(playbook_path='/opt/app/ansible/t.yml',extra_vars={"host":["10.120.180.1","10.120.180.2"],"name":"new_one"})
#     data = rbt.get_playbook_result()
