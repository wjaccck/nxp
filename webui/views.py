# coding=utf8
from django.shortcuts import redirect
from api.models import *
from proc.models import History_procs
from django.core.urlresolvers import reverse_lazy
import forms
import uuid
from core.common import getComStr,Cmd_ssh,\
    get_file_content,logger,pkey,generate_conf,vhost_j2,upstream_j2,\
    upstream_tmp_file,upstream_release_file,vhost_release_file,vhost_tmp_file,vhost_online_file,\
    upstream_online_file
from django.http import HttpResponseBadRequest,HttpResponseRedirect
from tasks import Run_ansible_redis_task
from abstract.views import Base_CreateViewSet, Base_ListViewSet, Base_UpdateViewSet,Base_DeleteViewSet,Base_Template,Base_Redirect
from datetime import timedelta, datetime


class IndexTemplateView(Base_Template):
    template_name = 'webui/index.html'

    def get_context_data(self, **kwargs):
        context=super(IndexTemplateView,self).get_context_data(**kwargs)
        # http_count = Site.objects.filter(https=False).count()
        # https_count = Site.objects.filter(https=True).count()
        # upstream_count = Upstream.objects.all().count()
        # public_count = Site.objects.filter(group=Nginx_group.objects.get(name='public')).count()
        # intra_count = Site.objects.filter(group=Nginx_group.objects.get(name='intra')).count()
        context['username']=self.request.user.last_name
        context['active']='index'
        # context['http_count']=http_count
        # context['https_count']=https_count
        # context['upstream_count']=upstream_count
        # context['public_count']=public_count
        # context['intra_count']=intra_count
        return context

class Status_CreateViewSet(Base_CreateViewSet):
    model = Status
    form_class = forms.StatusForm
    template_name = 'api/status_form.html'
    success_url = reverse_lazy('status-list')

class Status_UpdateViewSet(Base_UpdateViewSet):
    model = Status
    form_class = forms.StatusForm
    template_name = 'api/status_form.html'
    success_url = reverse_lazy('status-list')

class Status_ListViewSet(Base_ListViewSet):
    Status.objects.all().count()
    model = Status
    template_name = 'api/status.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name)
        else:
            return self.model.objects.all()
#
class Apps_ListViewSet(Base_ListViewSet):
    Apps.objects.all().count()
    model = Apps
    template_name = 'api/apps.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(host__icontains=name)
        else:
            return self.model.objects.all()

class Apps_CreateViewSet(Base_CreateViewSet):
    model = Apps
    form_class = forms.AppsForm
    template_name = 'api/apps_form.html'
    success_url = reverse_lazy('apps-list')

class Apps_UpdateViewSet(Base_UpdateViewSet):
    model = Apps
    form_class = forms.AppsForm
    template_name = 'api/apps_form.html'
    success_url = reverse_lazy('apps-list')

class Apps_group_ListViewSet(Base_ListViewSet):
    Apps_group.objects.all().count()
    model = Apps_group
    template_name = 'api/apps_group.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name)
        else:
            return self.model.objects.all()

class Apps_group_CreateViewSet(Base_CreateViewSet):
    model = Apps_group
    form_class = forms.Apps_groupForm
    template_name = 'api/apps_group_form.html'
    success_url = reverse_lazy('apps-group-list')

class Apps_group_UpdateViewSet(Base_UpdateViewSet):
    model = Apps_group
    form_class = forms.Apps_groupForm
    template_name = 'api/apps_group_form.html'
    success_url = reverse_lazy('apps-group-list')
#
class Group_CreateViewSet(Base_CreateViewSet):
    model = Nginx_group
    form_class = forms.Nginx_groupForm
    template_name = 'api/group_form.html'
    success_url = reverse_lazy('group-list')

class Group_UpdateViewSet(Base_UpdateViewSet):
    model = Nginx_group
    form_class = forms.Nginx_groupForm
    template_name = 'api/group_form.html'
    success_url = reverse_lazy('group-list')

class Group_ListViewSet(Base_ListViewSet):
    Nginx_group.objects.all().count()
    model = Nginx_group
    template_name = 'api/group.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name)
        else:
            return self.model.objects.all()
#
class Site_CreateViewSet(Base_CreateViewSet):
    model = Site
    form_class = forms.SiteForm
    template_name = 'api/site_form.html'
    success_url = reverse_lazy('site-list')

class Site_UpdateViewSet(Base_UpdateViewSet):
    model = Site
    form_class = forms.SiteForm
    template_name = 'api/site_form.html'
    success_url = reverse_lazy('site-list')

class Site_DeleteViewSet(Base_DeleteViewSet):
    model = Site
    success_url = reverse_lazy('site-list')

class Site_ListViewSet(Base_ListViewSet):
    Site.objects.all().count()
    model = Site
    template_name = 'api/site.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")
#
class Site_headers_CreateViewSet(Base_CreateViewSet):
    model = Site_headers
    form_class = forms.Site_headersForm
    template_name = 'api/site_headers_form.html'
    success_url = reverse_lazy('site-headers-list')

class Site_headers_UpdateViewSet(Base_UpdateViewSet):
    model = Site_headers
    form_class = forms.Site_headersForm
    template_name = 'api/site_headers_form.html'
    success_url = reverse_lazy('site-headers-list')

class Site_headers_DeleteViewSet(Base_DeleteViewSet):
    model = Site_headers
    success_url = reverse_lazy('site-headers-list')

class Site_headers_ListViewSet(Base_ListViewSet):
    Site_headers.objects.all().count()
    model = Site_headers
    template_name = 'api/site_headers.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")
#
class Proxy_headers_CreateViewSet(Base_CreateViewSet):
    model = Proxy_headers
    form_class = forms.Proxy_headersForm
    template_name = 'api/proxy_headers_form.html'
    success_url = reverse_lazy('proxy-headers-list')

class Proxy_headers_UpdateViewSet(Base_UpdateViewSet):
    model = Proxy_headers
    form_class = forms.Site_headersForm
    template_name = 'api/proxy_headers_form.html'
    success_url = reverse_lazy('proxy-headers-list')

class Proxy_headers_DeleteViewSet(Base_DeleteViewSet):
    model = Proxy_headers
    success_url = reverse_lazy('proxy-headers-list')

class Proxy_headers_ListViewSet(Base_ListViewSet):
    Proxy_headers.objects.all().count()
    model = Proxy_headers
    template_name = 'api/proxy_headers.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")
#
class Upstream_CreateViewSet(Base_CreateViewSet):
    model = Upstream
    form_class = forms.UpstreamForm
    template_name = 'api/upstream_form.html'
    success_url = reverse_lazy('upstream-list')

class Upstream_UpdateViewSet(Base_UpdateViewSet):
    model = Upstream
    form_class = forms.UpstreamForm
    template_name = 'api/upstream_form.html'
    success_url = reverse_lazy('upstream-list')

class Upstream_DeleteViewSet(Base_DeleteViewSet):
    model = Upstream
    success_url = reverse_lazy('upstream-list')

class Upstream_ListViewSet(Base_ListViewSet):
    Upstream.objects.all().count()
    model = Upstream
    template_name = 'api/upstream.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")
#
class Site_context_CreateViewSet(Base_CreateViewSet):
    model = Site_context
    form_class = forms.Site_contextForm
    template_name = 'api/context_form.html'
    success_url = reverse_lazy('context-list')

class Site_context_UpdateViewSet(Base_UpdateViewSet):
    model = Site_context
    form_class = forms.Site_contextForm
    template_name = 'api/context_form.html'
    success_url = reverse_lazy('context-list')

class Site_context_DeleteViewSet(Base_DeleteViewSet):
    model = Site_context
    success_url = reverse_lazy('context-list')

class Site_context_ListViewSet(Base_ListViewSet):
    Site_context.objects.all().count()
    model = Site_context
    template_name = 'api/context.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(site__name__istartswith=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")
                        #

class Redis_task_CreateViewSet(Base_CreateViewSet):
    model = Redis_task
    form_class = forms.Redis_taskForm
    template_name = 'api/redis_task_form.html'
    success_url = reverse_lazy('redis-task-list')

class Redis_tas_ListViewSet(Base_ListViewSet):
    Redis_task.objects.all().count()
    model = Redis_task
    template_name = 'api/redis_task.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(redis_host__name__istartswith=name)
        else:
            return self.model.objects.all()

class Run_redis_taskView(Base_Redirect):
    def get(self, request, *args, **kwargs):
        redis_task_id = self.kwargs.get('redis_task_id', None)
        task=Redis_task.objects.get(id=redis_task_id)
        task.status=Status.objects.get(name='in_queue')
        task.save()
        Run_ansible_redis_task().apply_async(args=(redis_task_id,))
        return HttpResponseRedirect('redis-task-list')

class Get_detailTemplate(Base_Template):
    template_name = 'api/detail.html'
    def get_context_data(self, **kwargs):
        context=super(Get_detailTemplate,self).get_context_data(**kwargs)
        site_id=self.kwargs.get('site_id',None)
        site=Site.objects.get(id=site_id)
        detail=[x for x in Site_context.objects.filter(site=site)]
        context['username']=self.request.user.last_name
        context['active']='nginx'
        context['site']=site.name
        context['detail']=detail
        context['site_id']=site_id
        return context

class Generate_vhostTemplate(Base_Template):
    template_name = 'api/conf.html'
    def get_context_data(self, **kwargs):
        context=super(Generate_vhostTemplate,self).get_context_data(**kwargs)
        file_list=[]
        site_id = self.kwargs.get('site_id', None)
        site=Site.objects.get(id=site_id)
        file_list.append(vhost_tmp_file.format(site.name))
        listen_port=''
        if site.http:
            listen_port=listen_port+'80 '
        if site.https:
            listen_port=listen_port+'ssl '
        if site.http2:
            listen_port=listen_port+'http2'

        if site.name.endswith('17shihui.com'):
            cer='_.17shihui.com.cer'
            key='_.17shihui.com.key'
        elif site.name.endswith('hiwemeet.com'):
            cer='_.hiwemeet.com.cer'
            key='_.hiwemeet.com.key'
        else:
            cer='_.hiwemeet.com.cer'
            key='_.hiwemeet.com.key'
        context_all=Site_context.objects.filter(site=site)
        info={
            "listen_port":listen_port,
            "https":site.https,
            "domain":site.name,
            "cer":cer,
            "key": key,
            "site_headers":[x.extra_parameter for x in site.extra_parameters.all()],
            "trace_status":site.trace_status,
            "context_all": [{
                "domain_proxy":y.upstream.domain_proxy,
                "app_name":y.upstream.name,
                "context":y.context,
                "default_proxy_set":y.default_proxy_set,
                "proxy_headers":[i.extra_parameter for i in y.extra_parametres.all()],
                "proxy_path":y.proxy_path
            }

                 for y in context_all]
        }
        vhost_result=generate_conf(vhost_j2,vhost_tmp_file.format(site.name),info)
        logger.info(vhost_result)
        upstreams=[x.upstream for x in context_all if x.upstream.status.name=='undo']
        for m in upstreams:
            upstream_info={
                "upstream":m.name,
                "ip_hash":m.ip_hash,
                "upstream_server":[x.__str__() for x in m.app.apps.all()]
            }
            upstream_result=generate_conf(upstream_j2,upstream_tmp_file.format(m.name),upstream_info)
            logger.info(upstream_result)
            file_list.append(upstream_tmp_file.format(m.name))

        new_content=''
        for n in file_list:
            new_content=new_content+"\r\n####%s####\r\n%s\r\n" %(n,get_file_content(n))

        context['active']="nginx"
        context['site']=site.name
        context['site_id']=site_id
        context['conf']=new_content
        return context

class Check_confTemplate(Base_Template):
    template_name = 'api/check.html'

    def get_context_data(self, **kwargs):
        context=super(Check_confTemplate,self).get_context_data(**kwargs)
        site_id = self.kwargs.get('site_id', None)
        all_status=True
        site = Site.objects.get(id=site_id)
        result =getComStr("rsync -av {0} {1}".format(vhost_tmp_file.format(site.name),vhost_release_file.format(site.name)))
        if result.get('retcode') != 0:
            all_status = False
            logger.error(result)
        detail = [x.upstream for x in Site_context.objects.filter(site=site) if x.upstream.app]
        upstreams=[ x for x in detail if x.status.name=='undo']
        for m in upstreams:
            result=getComStr("rsync -av {0} {1}".format(upstream_tmp_file.format(m.name), upstream_release_file.format(m.name)))
            if result.get('retcode') != 0:
                all_status=False
                logger.error(result)
        result =getComStr("/opt/app/nginx/sbin/nginx -t -c /opt/app/nginx/conf/nginx.conf")
        if result.get('retcode') != 0:
            all_status = False
            logger.error(result)
        context['username']=self.request.user.last_name
        context['active']='nginx'
        context['site']=site.name
        context['site_id']=site_id
        context['group']=site.group
        context['all_status']=all_status
        if all_status:
            context['content']='Check pass'
        else:
            context['content']='Check failed ! please check cmd.log'

        return context

class Create_tran_mission(Base_Redirect):
    def get(self, request, *args, **kwargs):
        site_id = self.kwargs.get('site_id', None)
        site=Site.objects.get(id=site_id)
        detail = [x.upstream for x in Site_context.objects.filter(site=site) if x.upstream.app]
        upstreams=[ x for x in detail if x.status.name=='undo']
        file_list = []
        for m in upstreams:
            file_list.append(upstream_online_file.format(m.name))
        file_list.append(vhost_online_file.format(site.name))
        mark=uuid.uuid4()
        for i in site.group.hosts.all():
            Nxp_mission.objects.create(site=site.name,
                                       mark=mark,
                                       host=i,
                                       files=','.join(file_list),
                                       status=Status.objects.get(name='undo')
                                       )
        return HttpResponseRedirect('/mission/?keyword={0}'.format(mark))

class Get_upstream_detailTemplate(Base_Template):
    template_name = 'api/upstream_detail.html'
    def get_context_data(self, **kwargs):
        context=super(Get_upstream_detailTemplate,self).get_context_data(**kwargs)
        upstream_id = self.kwargs.get('upstream_id', None)
        upstream=Upstream.objects.get(id=upstream_id)
        context['username']=self.request.user.last_name
        context['active']='nginx'
        context['upstream']=upstream
        return context

class Generate_upstream_confTemplate(Base_Template):
    template_name = 'api/upstream_conf.html'
    def get_context_data(self, **kwargs):
        context=super(Generate_upstream_confTemplate,self).get_context_data(**kwargs)
        upstream_id = self.kwargs.get('upstream_id', None)
        upstream=Upstream.objects.get(id=upstream_id)
        if upstream.domain_proxy:
            new_content='None'
        else:
            file_list=[]
            upstream_info = {
                "upstream": upstream.name,
                "ip_hash": upstream.ip_hash,
                "upstream_server": [x.__str__() for x in upstream.app.apps.all()]
            }
            upstream_result = generate_conf(upstream_j2, upstream_tmp_file.format(upstream.name), upstream_info)
            logger.info(upstream_result)
            file_list.append(upstream_tmp_file.format(upstream.name))
            new_content=''
            for m in file_list:
                new_content=new_content+"\r\n####%s####\r\n%s\r\n" %(m,get_file_content(m))
        context['username']=self.request.user.last_name
        context['active']='nginx'
        context['conf']=new_content
        context['upstream']=upstream
        return context

class Check_upstreamTemplate(Base_Template):
    template_name = 'api/upstream_check.html'
    def get_context_data(self, **kwargs):
        context=super(Check_upstreamTemplate,self).get_context_data(**kwargs)
        upstream_id = self.kwargs.get('upstream_id', None)
        upstream = Upstream.objects.get(id=upstream_id)
        all_status = True
        if upstream.domain_proxy:
            content='No need to check'
        else:
            result = getComStr("rsync -av {0} {1}".format(upstream_tmp_file.format(upstream.name),
                                                          upstream_release_file.format(upstream.name)))
            if result.get('retcode') != 0:
                all_status = False
                logger.error(result)
            result = getComStr("/opt/app/nginx/sbin/nginx -t -c /opt/app/nginx/conf/nginx.conf")
            if result.get('retcode') != 0:
                all_status = False
                logger.error(result)
            if all_status:
                content="Check pass"
            else:
                content="Check failed ! please check cmd.log"
        context['username']=self.request.user.last_name
        context['active']='nginx'
        context['content']=content
        context['upstream']=upstream
        return context

class Create_upstream_tran_mission(Base_Redirect):
    def get(self, request, *args, **kwargs):
        upstream_id = self.kwargs.get('upstream_id', None)
        upstream=Upstream.objects.get(id=upstream_id)
        file_list=[]
        if upstream.domain_proxy:
            response=HttpResponseBadRequest('No need to deploy')
        else:
            file_list.append(upstream_online_file.format(upstream.name))
            mark=uuid.uuid4()
            all_host=[]
            if upstream.group:
                all_host.extend(upstream.group.hosts.all())
            else:
                for m in Nginx_group.objects.filter(name='intra'):
                    all_host.extend(m.hosts.all())
                for m in Nginx_group.objects.filter(name='public'):
                    all_host.extend(m.hosts.all())
            for i in all_host:
                Nxp_mission.objects.create(
                                           mark=mark,
                                           host=i,
                                           files=','.join(file_list),
                                           status=Status.objects.get(name='undo')
                                           )
            response=HttpResponseRedirect('/mission/?keyword={0}'.format(mark))
        return response

class Tran_missionViewSet(Base_ListViewSet):
    Nxp_mission.objects.all().count()
    model = Nxp_mission
    template_name = 'api/nxp_mission.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(mark=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")

def Run_mission(req, mission_id):
    if req.user.is_authenticated():
        mission = Nxp_mission.objects.get(id=mission_id)

        ssh=Cmd_ssh(user='root',pkey=pkey,host=mission.host.name)
        for m in mission.files.split(','):
            m_result=ssh.upload(m,m)
            logger.info("{0} upload {1} to {2} {3}".format(mission.id,m,mission.host.name,m_result))
        result=ssh.run(' /opt/app/nginx/sbin/nginx -t -c /opt/app/nginx/conf/nginx.conf  && /etc/init.d/nginx reload')
        logger.info("{0} {1} reload nginx : {2}".format(mission.id,mission.host.name,result))
        if result.get('retcode')==0:
            if mission.site:
                for m in Site_context.objects.filter(site=Site.objects.get(name=mission.site)):
                    m.upstream.status=Status.objects.get(name='online')
                    m.upstream.save()

                mission.status=Status.objects.get(name='done')
                mission.remark=result.get('stdout')
            else:
                upstream_name=mission.files.split('/')[-1].split('.')[0]
                upstream=Upstream.objects.get(name=upstream_name)
                upstream.status=Status.objects.get(name='online')
                upstream.save()
                mission.status=Status.objects.get(name='done')
                mission.remark=result.get('stdout')
        else:
            mission.status=Status.objects.get(name='failed')
            mission.remark = result.get('stderr')
        mission.save()
        response = redirect('/mission/?keyword={0}'.format(mission.mark))
    else:
        response = redirect('login')
    return response

class Fun_queryTemplate(Base_Template):
    template_name = 'api/fun_query.html'
    def get_context_data(self, **kwargs):
        context=super(Fun_queryTemplate,self).get_context_data(**kwargs)
        try:
            name = self.request.GET['name']
            host = Ipv4Address.objects.get(name=name)
        except:
            host = None
        if host:
            info_status = True
            all_info=[]
            apps=host.app_host.all()
            for m in Upstream.objects.all():
                for n in m.app.apps.all():
                    if n in apps:
                        all_info.append({
                            "app":n,
                            "upstream":m,
                            "site_context":m.context_upstream.all()
                        })
            context['all_info']=all_info
            context['info_status']=info_status
        else:
            all_info = []
            info_status = False
            context['all_info']=all_info
            context['info_status']=info_status

        context['username']=self.request.user.last_name
        context['active']='nginx'
        return context

class Redis_instance_CreateViewSet(Base_CreateViewSet):
    model = Redis_instance
    form_class = forms.Redis_instanceForm
    template_name = 'api/redis_instance_form.html'
    success_url = reverse_lazy('redis-instance-list')

class Redis_instance_UpdateViewSet(Base_UpdateViewSet):
    model = Redis_instance
    form_class = forms.Redis_instanceForm
    template_name = 'api/redis_instance_form.html'
    success_url = reverse_lazy('redis-instance-list')

class Redis_instance_DeleteViewSet(Base_DeleteViewSet):
    model = Redis_instance
    success_url = reverse_lazy('redis-instance-list')

class Redis_instance_ListViewSet(Base_ListViewSet):
    Redis_instance.objects.all().count()
    model = Redis_instance
    template_name = 'api/redis_instance.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(host__name__istartswith=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")

class Redis_group_CreateViewSet(Base_CreateViewSet):
    model = Redis_group
    form_class = forms.Redis_groupForm
    template_name = 'api/redis_group_form.html'
    success_url = reverse_lazy('redis-group-list')

class Redis_group_UpdateViewSet(Base_UpdateViewSet):
    model = Redis_group
    form_class = forms.Redis_groupForm
    template_name = 'api/redis_group_form.html'
    success_url = reverse_lazy('redis-group-list')

class Redis_group_DeleteViewSet(Base_DeleteViewSet):
    model = Redis_group
    success_url = reverse_lazy('redis-group-list')

class Redis_group_ListViewSet(Base_ListViewSet):
    Redis_group.objects.all().count()
    model = Redis_group
    template_name = 'api/redis_group.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")

class Codis_CreateViewSet(Base_CreateViewSet):
    model = Codis
    form_class = forms.CodisForm
    template_name = 'api/codis_form.html'
    success_url = reverse_lazy('codis-list')

class Codis_UpdateViewSet(Base_UpdateViewSet):
    model = Codis
    form_class = forms.CodisForm
    template_name = 'api/codis_form.html'
    success_url = reverse_lazy('codis-list')

class Codis_DeleteViewSet(Base_DeleteViewSet):
    model = Codis
    success_url = reverse_lazy('codis-list')

class Codis_ListViewSet(Base_ListViewSet):
    Codis.objects.all().count()
    model = Codis
    template_name = 'api/codis.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")

            #

class Sentinel_ListViewSet(Base_ListViewSet):
    Sentinel.objects.all().count()
    model = Sentinel
    template_name = 'api/sentinel.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
        else:
            return self.model.objects.all().order_by("-modified_date")

class Codis_detailTemplate(Base_Template):
    template_name = 'api/codis-detail.html'
    def get_context_data(self, **kwargs):
        context=super(Codis_detailTemplate,self).get_context_data(**kwargs)
        try:
            codis_id = self.kwargs.get('codis_id', None)
            codis=Codis.objects.get(id=codis_id)
        except:
            codis=None

        if codis:
            all_info = codis.member.all()
            context['codis'] = codis.name
        else:
            all_info = []
            context['codis'] = 'not existed this codis'

        context['username']=self.request.user.last_name
        context['active']='redis'
        context['all_info']=all_info
        return context

class Sentinel_detailTemplate(Base_Template):
    template_name = 'api/sentinel-detail.html'
    def get_context_data(self, **kwargs):
        context=super(Sentinel_detailTemplate,self).get_context_data(**kwargs)
        try:
            sentinel_id = self.kwargs.get('sentinel_id', None)
            sentinel=Codis.objects.get(id=sentinel_id)
        except:
            sentinel=None

        if sentinel:
            all_info = sentinel.member.all()
            context['sentinel'] = sentinel.name
        else:
            all_info = []
            context['sentinel'] = 'not existed this sentinel'

        context['username']=self.request.user.last_name
        context['active']='redis'
        context['all_info']=all_info
        return context

class Codis_queryTemplate(Base_Template):
    template_name = 'api/query-detail.html'
    def get_context_data(self, **kwargs):
        context=super(Codis_queryTemplate,self).get_context_data(**kwargs)
        try:
            name = self.request.GET['name']
            host = Ipv4Address.objects.get(name=name)
        except:
            host=None

        if host:
            redis_instrance=Redis_instance.objects.filter(host=host)
            host_name=host.name
            group_master=[]
            group_offline=[]
            group_slave=[]
            for m in redis_instrance:
                for n in Redis_group.objects.filter(master=m):
                    group_master.append({"group":n,"host":host_name,"port":m.port})
            for m in redis_instrance:
                for n in Redis_group.objects.filter(offline=m):
                    group_offline.append({"group":n,"host":host_name,"port":m.port})

            for m in redis_instrance:
                for n in Redis_group.objects.filter(slave=m):
                    group_slave.append({"group":n,"host":host_name,"port":m.port})
            # codis
            codis_master=[{"codis":x.get("group").codis_group.all(),"group":x.get("group"),"host":x.get("host"),"name":"master","port":x.get("port")} for x in group_master]
            codis_offline=[{"codis":x.get("group").codis_group.all(),"group":x.get("group"),"host":x.get("host"),"name":"offline","port":x.get("port")} for x in group_offline]
            codis_slave=[{"codis":x.get("group").codis_group.all(),"group":x.get("group"),"host":x.get("host"),"name":"slave","port":x.get("port")} for x in group_slave]

            #sentinel
            sentinel_master=[{"sentinel":x.get("group").sentinel_group.all(),"group":x.get("group"),"host":x.get("host"),"name":"master","port":x.get("port")} for x in group_master]
            sentinel_offline=[{"sentinel":x.get("group").sentinel_group.all(),"group":x.get("group"),"host":x.get("host"),"name":"offline","port":x.get("port")} for x in group_offline]
            sentinel_slave=[{"sentinel":x.get("group").sentinel_group.all(),"group":x.get("group"),"host":x.get("host"),"name":"slave","port":x.get("port")} for x in group_slave]
        else:
            # codis
            codis_master=[]
            codis_offline=[]
            codis_slave=[]
            #sentinel
            sentinel_master=[]
            sentinel_offline=[]
            sentinel_slave=[]
        context['username']=self.request.user.last_name
        context['active']='redis'
        context['codis_master']=codis_master
        context['codis_slave']=codis_slave
        context['codis_offline']=codis_offline
        context['sentinel_master']=sentinel_master
        context['sentinel_slave']=sentinel_slave
        context['sentinel_offline']=sentinel_offline
        return context

class Http_request_countTemplate(Base_Template):
    template_name = 'api/chart.html'
    def get_context_data(self, **kwargs):
        context=super(Http_request_countTemplate,self).get_context_data(**kwargs)
        try:
            name=self.request.GET['domain'].strip()
        except:
            name=None
        def get_total(daytime,domain=None):
            if domain:
                data=Http_statistics.objects.filter(daytime=daytime,domain=domain)
            else:
                data = Http_statistics.objects.filter(daytime=daytime)
            total_data=[x.Unknown_status+x.success_status+x.client_err_status+x.server_err_status for x in data]
            return sum(total_data).__int__()
        def get_unknown(daytime,domain=None):
            if domain:
                data=Http_statistics.objects.filter(daytime=daytime,domain=domain)
            else:
                data = Http_statistics.objects.filter(daytime=daytime)
            unknown_data=[x.Unknown_status for x in data]
            return sum(unknown_data).__int__()
        def get_success(daytime,domain=None):
            if domain:
                data=Http_statistics.objects.filter(daytime=daytime,domain=domain)
            else:
                data = Http_statistics.objects.filter(daytime=daytime)
            success_data=[x.success_status for x in data]
            return sum(success_data).__int__()
        def get_client_err(daytime,domain=None):
            if domain:
                data=Http_statistics.objects.filter(daytime=daytime,domain=domain)
            else:
                data = Http_statistics.objects.filter(daytime=daytime)
            client_err_data=[x.client_err_status for x in data]
            return sum(client_err_data).__int__()
        def get_server_err(daytime,domain=None):
            if domain:
                data=Http_statistics.objects.filter(daytime=daytime,domain=domain)
            else:
                data = Http_statistics.objects.filter(daytime=daytime)
            server_err_data=[x.server_err_status for x in data]
            return sum(server_err_data).__int__()

        time_line=[]
        for m in range(1,8):
            p_day = datetime.today() + timedelta(-m)
            p_day_format = p_day.strftime('%Y%m%d')
            time_line.append(p_day_format)
        time_line.reverse()
        unknown_count=[get_unknown(x,name) for x in time_line]
        client_err_count=[get_client_err(x,name) for x in time_line]
        server_err_count=[get_server_err(x,name) for x in time_line]
        success_count=[get_success(x,name) for x in time_line]
        total_count=[get_total(x,name) for x in time_line]
        context['timeline']=time_line
        context['domain']=name
        context['active']='nginx'
        context['unknown_count']=unknown_count
        context['client_err_count']=client_err_count
        context['server_err_count']=server_err_count
        context['success_count']=success_count
        context['total_count']=total_count
        return context

class Http_request_statisticsTemplate(Base_Template):
    template_name = 'api/avg.html'
    def get_context_data(self, **kwargs):
        context=super(Http_request_statisticsTemplate,self).get_context_data(**kwargs)
        try:
            limit=self.request.GET['limit']
        except:
            limit=100
        def get_total(daytime, domain=None):
            data = Http_statistics.objects.filter(daytime=daytime, domain=domain)
            total_data = [x.Unknown_status + x.success_status + x.client_err_status + x.server_err_status for x in
                          data]
            return sum(total_data).__int__()
        time_line = []
        for m in range(1, 8):
            p_day = datetime.today() + timedelta(-m)
            p_day_format = p_day.strftime('%Y%m%d')
            time_line.append(p_day_format)
        domain_list=[x.get('domain') for x in Http_statistics.objects.distinct().values('domain') if 'weimi.me' not in x.get('domain')]

        all_info=[]
        for m in domain_list:
            avg=None
            avg=sum([get_total(x,m) for x in time_line])/7
            if avg<limit:
                all_info.append({"domain":m,"avg":avg})

        avg_list = sorted(all_info, key=lambda all_info: (all_info['avg']), reverse=False)
        context['all_info']=avg_list
        context['avg_count']=avg_list.__len__()
        context['limit']=limit
        return context


class Historyprocs_ListViewSet(Base_ListViewSet):
    History_procs.objects.all().count()
    model = History_procs
    template_name = 'api/procs.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(host=name)
        else:
            return self.model.objects.all()