# coding=utf8
from django.db.models import Q
from django.shortcuts import render,redirect
from api.models import *
from django.core.urlresolvers import reverse_lazy
import forms
import uuid
from core.common import getComStr,head_file,tail_file,context_file,upstream_file,Cmd_ssh,\
    get_file_content,logger,pkey,redirect_file,generate_conf,vhost_j2,upstream_j2,\
    upstream_tmp_file,upstream_release_file,vhost_release_file,vhost_tmp_file,vhost_online_file,\
    upstream_online_file,shihui_https_file,hiwemeet_https_file,ssl_vhost_online_file,ssl_vhost_release_file,ssl_vhost_tmp_file
from django.http import HttpResponse,HttpResponseBadRequest,StreamingHttpResponse
from tasks import Run_ansible_redis_task
from abstract.views import Base_CreateViewSet, Base_ListViewSet, Base_UpdateViewSet,Base_DeleteViewSet,Base_Template
from datetime import timedelta, datetime


class IndexTemplateView(Base_Template):
    template_name = 'webui/index.html'

    def get_context_data(self, **kwargs):
        context=super(IndexTemplateView,self).get_context_data(**kwargs)
        http_count = Site.objects.filter(https=False).count()
        https_count = Site.objects.filter(https=True).count()
        upstream_count = Upstream.objects.all().count()
        public_count = Site.objects.filter(group=Nginx_group.objects.get(name='public')).count()
        intra_count = Site.objects.filter(group=Nginx_group.objects.get(name='intra')).count()
        context['username']=self.request.user.last_name
        context['active']='index'
        context['http_count']=http_count
        context['https_count']=https_count
        context['upstream_count']=upstream_count
        context['public_count']=public_count
        context['intra_count']=intra_count
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

def Run_redis_task(req,redis_task_id):
    if req.user.is_authenticated():
        task=Redis_task.objects.get(id=redis_task_id)
        task.status=Status.objects.get(name='in_queue')
        task.save()
        Run_ansible_redis_task().apply_async(args=(redis_task_id,))
        response = redirect('redis-task-list')
    else:
        response =redirect('login')
    return response

class Get_detailTemplate(Base_Template):
    template_name = 'api/detail.html'
    # def get(self, request, *args, **kwargs):
    #     site_id=self.kwargs.get('site_id',None)
    #     context=self.get_context_data(**kwargs)
    #     return self.render_to_response(context)
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

# def Get_detail(req,site_id):
#     if req.user.is_authenticated():
#         site=Site.objects.get(id=site_id)
#         detail=[x for x in Site_context.objects.filter(site=site)]
#
#         response = render(req,'api/detail.html',{"username":req.user.last_name,
#                                                   "active":"nginx",
#                                                    "site":site.name,
#                                                    "detail":detail,
#                                                     "site_id":site_id
#                                                   }
#                           )
#     else:
#         response =redirect('login')
#     return response

class Generate_vhostTemplate(Base_Template):
    template_name = 'api/conf.html'
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        return self.render_to_response()
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
            "domain":site.name,
            "cer":cer,
            "key": key,
            "site_headers":[x.extra_parameter for x in site.extra_parameters.all()],
            "trace_status":site.trace_status,
            "context_all": [{
                "domain_proxy":y.upstream.domain_proxy,
                "app_name":y.upstream.app.name,
                "context":y.context,
                "default_proxy_set":y.default_proxy_set,
                "proxy_headers":[i.extra_parameter for i in y.extra_parametres.all()],
                "proxy_path":y.proxy_path
            }

                 for y in context_all]
        }
        vhost_result=generate_conf(vhost_j2,vhost_tmp_file.format(site.name),info)
        logger.info(vhost_result)
        upstreams=[x.upstream for x in context_all if cmp(x.upstream.status.name,'undo')]
        for m in upstreams:
            upstream_result=generate_conf(upstream_j2,upstream_tmp_file,m)
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
#
# def Generate_conf(req, site_id):
#     if req.user.is_authenticated():
#         site = Site.objects.get(id=site_id)
#         file_list = []
#         if site.redirect_status:
#             content = get_file_content(redirect_file)
#             vhost_tmp_conf = open(vhost_tmp_file.format(site.name), 'w')
#             vhost_tmp_conf.write(content.replace('http_host', site.name))
#             vhost_tmp_conf.write('\r\n    ')
#             for m in Site_headers.objects.filter(site=site):
#                 vhost_tmp_conf.write(';\r\n        '.join(m.extra_conf.__str__().split(';')))
#             vhost_tmp_conf.close()
#         else:
#             detail = [x for x in Site_context.objects.filter(site=site)]
#             ## get template for nginx vhost and upstream
#             if site.https:
#                 if site.name.endswith('17shihui.com'):
#                     head_content = get_file_content(shihui_https_file)
#                 else:
#                     head_content = get_file_content(hiwemeet_https_file)
#             else:
#                 head_content=get_file_content(head_file)
#             context_content=get_file_content(context_file)
#             tail_content = get_file_content(tail_file)
#             upstream_content = get_file_content(upstream_file)
#
#             upstreams=[ x.upstream for x in detail if x.upstream.status.name=='undo']
#
#             for m in upstreams:
#                 m_content=None
#                 if m.direct_status:
#                     pass
#                 else:
#                     upstream_tmp_conf=open(upstream_tmp_file.format(m.name),'w')
#                     m_content=upstream_content.replace('upstream_name',m.name)
#                     back_end_list=[ "server {0}:{1};".format(x.name,m.port) for x in m.hosts.all()]+["server {0}:{1};".format(x.host.name,x.port) for x in m.docker_list.all()]
#                     if m.ip_hash:
#                         back_end_list.insert(0,'ip_hash;')
#                     m_content=m_content.replace('back_end','\n    '.join(back_end_list))
#                     upstream_tmp_conf.write(m_content)
#                     upstream_tmp_conf.close()
#                     logger.info("create upstream conf {0}".format(upstream_tmp_file.format(m.name)))
#                     file_list.append(upstream_tmp_file.format(m.name))
#             if site.https:
#                 vhost_tmp_conf=open(ssl_vhost_tmp_file.format(site.name),'w')
#             else:
#                 vhost_tmp_conf=open(vhost_tmp_file.format(site.name),'w')
#
#             vhost_tmp_conf.write(head_content.replace('http_host',site.name))
#             vhost_tmp_conf.write('\r\n    ')
#             for n in Site_headers.objects.filter(site=site):
#                 vhost_tmp_conf.write(';\r\n        '.join(n.extra_conf.split(';')))
#             for m in detail:
#                 m_content=context_content.replace('context_path',m.context)
#                 if m.upstream:
#                     if m.proxy_path:
#                         m_upstream_name=m.upstream.name.strip()+m.proxy_path.strip()
#                     else:
#                         m_upstream_name=m.upstream.name
#                     m_content=m_content.replace('upstream_name',m_upstream_name)
#                 else:
#                     m_content=m_content.replace('proxy_pass  http://upstream_name;','')
#                 m_parametres=[x.strip() for x in m.extra_parametres.split(';')]
#                 if m.default_proxy_set:
#                     m_parametres.insert(0,'include proxy_conf')
#                 if m.lua_status:
#                     m_parametres.insert(1,'log_by_lua_file /opt/nginx/conf/status/kafka.lua')
#                 m_content=m_content.replace('extra_parametres',';\r\n        '.join(m_parametres))
#                 vhost_tmp_conf.write(m_content)
#
#             vhost_tmp_conf.write(tail_content)
#             vhost_tmp_conf.close()
#         if site.https:
#             logger.info("create upstream conf {0}".format(ssl_vhost_tmp_file.format(site.name)))
#             file_list.append(ssl_vhost_tmp_file.format(site.name))
#         else:
#             logger.info("create upstream conf {0}".format(vhost_tmp_file.format(site.name)))
#             file_list.append(vhost_tmp_file.format(site.name))
#
#         new_content=''
#         for m in file_list:
#             new_content=new_content+"\r\n####%s####\r\n%s\r\n" %(m,get_file_content(m))
#
#         response = render(req, 'api/conf.html', {"username": req.user.last_name,
#                                                    "active": "nginx",
#                                                    "conf": new_content,
#                                                     "site": site.name,
#                                                     "site_id": site_id
#                                                    }
#                           )
#     else:
#         response = redirect('login')
#     return response

def Conf_check(req, site_id):
    if req.user.is_authenticated():
        all_status=True
        site = Site.objects.get(id=site_id)
        if site.https:
            result =getComStr("rsync -av {0} {1}".format(ssl_vhost_tmp_file.format(site.name),ssl_vhost_release_file.format(site.name)))
        else:
            result =getComStr("rsync -av {0} {1}".format(vhost_tmp_file.format(site.name),vhost_release_file.format(site.name)))
        if result.get('retcode') != 0:
            all_status = False
            logger.error(result)
        detail = [x for x in Site_context.objects.filter(site=site)]
        upstreams=[ x.upstream for x in detail if x.upstream.status.name=='undo']
        for m in upstreams:
            if not m.direct_status:
                result=getComStr("rsync -av {0} {1}".format(upstream_tmp_file.format(m.name), upstream_release_file.format(m.name)))
                if result.get('retcode') != 0:
                    all_status=False
                    logger.error(result)
        # if site.https:
        #     result=getComStr("rsync -av {0} {1}".format(ssl_vhost_release_file.format(site.name),ssl_vhost_online_file.format(site.name)))
        # else:
        #     result=getComStr("rsync -av {0} {1}".format(vhost_release_file.format(site.name),vhost_online_file.format(site.name)))
        # if result.get('retcode') != 0:
        #     all_status = False
        #     logger.error(result)
        # for m in upstreams:
        #     result=getComStr("rsync -av {0} {1}".format(upstream_release_file.format(m.name), upstream_online_file.format(m.name)))
        #     if result.get('retcode') != 0:
        #         all_status=False
        #         logger.error(result)
        result =getComStr("/opt/nginx/sbin/nginx -t -c /opt/nginx/conf/nginx.conf")
        if result.get('retcode') != 0:
            all_status = False
            logger.error(result)
        if all_status:
            response = render(req, 'api/check.html', {"username": req.user.last_name,
                                                       "active": "nginx",
                                                       "site": site.name,
                                                       "site_id": site_id,
                                                       "group":site.group,
                                                       "content":"Check pass",
                                                       "all_status":all_status
                                                       }
                              )
        else:
            response = render(req, 'api/check.html', {"username": req.user.last_name,
                                                       "active": "nginx",
                                                       "site": site.name,
                                                       "site_id": site_id,
                                                       "content":"Check failed ! please check cmd.log",
                                                        "all_status":all_status
                                                       }
                              )
    else:
        response = redirect('login')
    return response

def Create_tran_mission(req, site_id):
    if req.user.is_authenticated():
        site = Site.objects.get(id=site_id)
        detail = [x for x in Site_context.objects.filter(site=site)]
        file_list = []
        ## get template for nginx vhost and upstream
        upstreams=[ x.upstream for x in detail if x.upstream.status.name=='undo']

        file_list=[]

        for m in upstreams:
            if not m.direct_status:
                file_list.append(upstream_online_file.format(m.name))
        if site.https:
            file_list.append(ssl_vhost_online_file.format(site.name))
        else:
            file_list.append(vhost_online_file.format(site.name))

        mark=uuid.uuid4()
        for i in site.group.hosts.all():
            Nxp_mission.objects.create(site=site,
                                       mark=mark,
                                       host=i,
                                       files=','.join(file_list),
                                       status=Status.objects.get(name='undo')
                                       )



        response = redirect('/mission/?keyword={0}'.format(mark))
    else:
        response = redirect('login')
    return response

def Get_upstream_detail(req,upstream_id):
    if req.user.is_authenticated():
        upstream=Upstream.objects.get(id=upstream_id)
        response = render(req,'api/upstream_detail.html',{"username":req.user.last_name,
                                                  "active":"nginx",
                                                   "upstream":upstream,
                                                  }
                          )
    else:
        response =redirect('login')
    return response

def Generate_upstream_conf(req, upstream_id):
    if req.user.is_authenticated():
        upstream = Upstream.objects.get(id=upstream_id)
        file_list = []
        upstream_content = get_file_content(upstream_file)

        if upstream.direct_status:
            pass
        else:
            upstream_tmp_conf=open(upstream_tmp_file.format(upstream.name),'w')
            upstream_content=upstream_content.replace('upstream_name',upstream.name)
            back_end_list=[ "server {0}:{1};".format(x.name,upstream.port) for x in upstream.hosts.all()]+["server {0}:{1};".format(x.host.name,x.port) for x in upstream.docker_list.all()]
            if upstream.ip_hash:
                back_end_list.insert(0,'ip_hash;')
            upstream_content=upstream_content.replace('back_end','\n    '.join(back_end_list))
            upstream_tmp_conf.write(upstream_content)
            upstream_tmp_conf.close()
            logger.info("create upstream conf {0}".format(upstream_tmp_file.format(upstream.name)))
            file_list.append(upstream_tmp_file.format(upstream.name))

        new_content=''
        for m in file_list:
            new_content=new_content+"\r\n####%s####\r\n%s\r\n" %(m,get_file_content(m))

        response = render(req, 'api/upstream_conf.html', {"username": req.user.last_name,
                                                   "active": "nginx",
                                                   "conf": new_content,
                                                    "upstream": upstream,
                                                   }
                          )
    else:
        response = redirect('login')
    return response

def Conf_upstream_check(req, upstream_id):
    if req.user.is_authenticated():
        all_status=True
        upstream=Upstream.objects.get(id=upstream_id)
        if not upstream.direct_status:
            result=getComStr("rsync -av {0} {1}".format(upstream_tmp_file.format(upstream.name), upstream_release_file.format(upstream.name)))
            if result.get('retcode') != 0:
                all_status=False
                logger.error(result)
        result =getComStr("/opt/nginx/sbin/nginx -t -c /opt/nginx/conf/nginx.conf")
        if result.get('retcode') != 0:
            all_status = False
            logger.error(result)
        if all_status:
            response = render(req, 'api/upstream_check.html', {"username": req.user.last_name,
                                                       "active": "nginx",
                                                       "upstream": upstream,
                                                       "content":"Check pass",
                                                       "all_status":all_status
                                                       }
                              )
        else:
            response = render(req, 'api/upstream_check.html', {"username": req.user.last_name,
                                                       "active": "nginx",
                                                       "upstream": upstream,
                                                       "content":"Check failed ! please check cmd.log",
                                                        "all_status":all_status
                                                       }
                              )
    else:
        response = redirect('login')
    return response

def Create_upstream_tran_mission(req, upstream_id):
    if req.user.is_authenticated():
        upstream=Upstream.objects.get(id=upstream_id)
        file_list=[]

        if not upstream.direct_status:
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



        response = redirect('/mission/?keyword={0}'.format(mark))
    else:
        response = redirect('login')
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
        result=ssh.run(' /opt/nginx/sbin/nginx -t -c /opt/nginx/conf/nginx.conf  && /etc/init.d/nginx reload')
        logger.info("{0} {1} reload nginx : {2}".format(mission.id,mission.host.name,result))
        if result.get('retcode')==0:
            if mission.site:
                for m in Site_context.objects.filter(site=mission.site):
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

def Fun_queryView(req):
    if req.user.is_authenticated():
        try:
            name=req.GET['name']
        except:
            name=None

        if name:
            info_status = True
            host = Ipv4Address.objects.get(name=name)
            upstreams=host.upstream_host.all()
            # site=[{"host":host,"site_all":x.context_upstream.all(),"upstream":x} for x in upstreams]
            # context['all_info'] = map(lambda x: {"host": name, "upstream": x.name, "site": x.context_upstream.all()},
            #                           host.upstream_host.all())
            all_info = [{"host":host,"site_all":x.context_upstream.all(),"upstream":x} for x in upstreams]
        else:
            all_info = []
            info_status = False
        response = render(req, 'api/fun_query.html', {"username": req.user.last_name,
                                                   "active": "nginx",
                                                   "info_status":info_status,
                                                   "all_info":all_info
                                                   }
                          )
    else:
        response = redirect('login')
    return response


#### redis views



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



def Codis_detailView(req,codis_id):
    if req.user.is_authenticated():
        try:
            codis=Codis.objects.get(id=codis_id)
        except:
            codis=None

        if codis:
            all_info=codis.member.all()
            response = render(req, 'api/codis-detail.html', {"username": req.user.last_name,
                                                             "active": "redis",
                                                             "all_info": all_info,
                                                             "codis": codis.name
                                                             }
                              )
        else:
            response = HttpResponseBadRequest("not existed this codis")
    else:
        response = redirect('login')
    return response




def Sentinel_detailView(req,sentinel_id):
    if req.user.is_authenticated():
        try:
            sentinel=Sentinel.objects.get(id=sentinel_id)
        except:
            sentinel=None

        if sentinel:
            all_info=sentinel.member.all()
            response = render(req, 'api/sentinel-detail.html', {"username": req.user.last_name,
                                                             "active": "redis",
                                                             "all_info": all_info,
                                                             "sentinel": sentinel.name
                                                             }
                              )
        else:
            response = HttpResponseBadRequest("not existed this sentinel")
    else:
        response = redirect('login')
    return response

def Codis_queryView(req):
    if req.user.is_authenticated():
        try:
            name = req.GET['name']
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

            response = render(req, 'api/query-detail.html', {"username": req.user.last_name,
                                                             "active": "redis",
                                                             "codis_master": codis_master,
                                                             "codis_slave": codis_slave,
                                                             "codis_offline": codis_offline,
                                                             "sentinel_master": sentinel_master,
                                                             "sentinel_slave": sentinel_slave,
                                                             "sentinel_offline": sentinel_offline,
                                                             }
                              )
        else:
            response = render(req, 'api/query-detail.html', {"username": req.user.last_name,
                                                             "active": "redis",
                                                             "codis_master": [],
                                                             "codis_slave": [],
                                                             "codis_offline": [],
                                                             "sentinel_master": [],
                                                             "sentinel_slave": [],
                                                             "sentinel_offline": [],
                                                             }
                              )
    else:
        response = redirect('login')
    return response

def Http_request_countView(req):
    if req.user.is_authenticated():
        try:
            name=req.GET['domain'].strip()
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
        response = render(req, 'api/chart.html', {
                                                    "timeline": time_line,
                                                    "domain":name,
                                                    "active": "nginx",
                                                    "unknown_count":unknown_count,
                                                    "client_err_count":client_err_count,
                                                    "server_err_count":server_err_count,
                                                    "success_count":success_count,
                                                    "total_count":total_count
                                                   }
                          )
    else:
        response = redirect('login')
    return response



def Http_request_statisticsView(req):
    if req.user.is_authenticated():
        try:
            limit=req.GET['limit']
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
        response = render(req, 'api/avg.html', {
                                                    "all_info":avg_list,
                                                    "avg_count":avg_list.__len__(),
                                                    "limit":limit
                                                   }
                          )
    else:
        response = redirect('login')
    return response

#
# class Http_request_ListViewSet(Base_ListViewSet):
#     Redis_group.objects.all().count()
#     model = Redis_group
#     template_name = 'api/request_count.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         try:
#             limit = int(self.request.GET['keyword'])
#         except:
#             limit = 100
#         time_line=[]
#         for m in range(1,8):
#             p_day = datetime.today() + timedelta(-m)
#             p_day_format = p_day.strftime('%Y%m%d')
#             time_line.append(p_day_format)
#         time_line.reverse()
#
#         all_domain=[x.get('domain') for x in Http_statistics.objects.distinct().values('domain')]
#
#         def get_statistics(s_data):
#             ret_status=True
#             for i in s_data:
#                 i_total=i.Unknown_status+i.success_status+i.client_err_status+i.server_err_status
#                 if i_total>limit:
#                     ret_status=False
#
#             return ret_status
#
#         for n in all_domain:
#             for p in time_line:
#                 if get_statistics(Http_statistics.objects.filter(domain=n,daytime=p)):
#
#
#
#         try:
#             name = self.request.GET['keyword']
#         except:
#             pass
#
#         if name:
#             return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
#         else:
#             return self.model.objects.all().order_by("-modified_date")