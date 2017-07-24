__author__ = 'jinhongjun'
import logging
logger = logging.getLogger("nxp")
import commands
import paramiko

pkey='/root/.ssh/id_rsa'
head_file="/opt/app/nxp/templates/nginx/head.conf"
shihui_https_file="/opt/app/nxp/templates/nginx/17shihui_https.conf"
hiwemeet_https_file="/opt/app/nxp/templates/nginx/hiwemeet_https.conf"
context_file="/opt/app/nxp/templates/nginx/context.conf"
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