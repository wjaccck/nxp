# coding=utf8
from django.db.models import Q
from django.shortcuts import render,redirect
from api.models import *
from django.core.urlresolvers import reverse_lazy
import forms
import uuid
from core.common import getComStr,head_file,tail_file,context_file,upstream_file,Cmd_ssh,\
    get_file_content,logger,pkey,\
    upstream_tmp_file,upstream_release_file,vhost_release_file,vhost_tmp_file,vhost_online_file,\
    upstream_online_file,shihui_https_file,hiwemeet_https_file,ssl_vhost_online_file,ssl_vhost_release_file,ssl_vhost_tmp_file
from django.http import HttpResponse,HttpResponseBadRequest,StreamingHttpResponse
import operator
# from tasks import MissionTask
from vanilla import TemplateView
from abstract.views import Base_CreateViewSet, Base_ListViewSet, Base_UpdateViewSet,Base_DeleteViewSet


def index(req):
    if req.user.is_authenticated():

        response = render(req,'webui/index.html',{"username":req.user.last_name,
                                                  "active":"index"
                                                  }
                          )
    else:
        response =redirect('login')
    return response

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
class Group_CreateViewSet(Base_CreateViewSet):
    model = Group
    form_class = forms.GroupForm
    template_name = 'api/group_form.html'
    success_url = reverse_lazy('group-list')

class Group_UpdateViewSet(Base_UpdateViewSet):
    model = Group
    form_class = forms.GroupForm
    template_name = 'api/group_form.html'
    success_url = reverse_lazy('group-list')

class Group_ListViewSet(Base_ListViewSet):
    Group.objects.all().count()
    model = Group
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
            return self.model.objects.filter(site__name__istartswith=name)
        else:
            return self.model.objects.all()
                        #



def Get_detail(req,site_id):
    if req.user.is_authenticated():
        site=Site.objects.get(id=site_id)
        detail=[x for x in Site_context.objects.filter(site=site)]

        response = render(req,'api/detail.html',{"username":req.user.last_name,
                                                  "active":"nginx",
                                                   "site":site.name,
                                                   "detail":detail,
                                                    "site_id":site_id
                                                  }
                          )
    else:
        response =redirect('login')
    return response

def Generate_conf(req, site_id):
    if req.user.is_authenticated():
        site = Site.objects.get(id=site_id)
        detail = [x for x in Site_context.objects.filter(site=site)]
        file_list = []
        ## get template for nginx vhost and upstream
        if site.https:
            if site.name.endswith('17shihui.com'):
                head_content = get_file_content(shihui_https_file)
            else:
                head_content = get_file_content(hiwemeet_https_file)
        else:
            head_content=get_file_content(head_file)
        context_content=get_file_content(context_file)
        tail_content = get_file_content(tail_file)
        upstream_content = get_file_content(upstream_file)

        upstreams=[ x.upstream for x in detail if x.upstream.status.name=='undo']

        file_list=[]

        for m in upstreams:
            m_content=None
            if m.direct_status:
                pass
            else:
                upstream_tmp_conf=open(upstream_tmp_file.format(m.name),'w')
                m_content=upstream_content.replace('upstream_name',m.name)
                m_content=m_content.replace('back_end','\n    '.join([ "server {0}:{1};".format(x.name,m.port) for x in m.hosts.all()]))
                upstream_tmp_conf.write(m_content)
                upstream_tmp_conf.close()
                logger.info("create upstream conf {0}".format(upstream_tmp_file.format(m.name)))
                file_list.append(upstream_tmp_file.format(m.name))
        if site.https:
            vhost_tmp_conf=open(ssl_vhost_tmp_file.format(site.name),'w')
        else:
            vhost_tmp_conf=open(vhost_tmp_file.format(site.name),'w')

        vhost_tmp_conf.write(head_content.replace('http_host',site.name))
        for m in detail:
            m_content=context_content.replace('context_path',m.context)
            m_content=m_content.replace('upstream_name',m.upstream.name)
            m_content=m_content.replace('extra_parametres',';\r\n        '.join([ x.strip() for x in m.extra_parametres.split(';')]))
            vhost_tmp_conf.write(m_content)

        vhost_tmp_conf.write(tail_content)
        vhost_tmp_conf.close()
        if site.https:
            logger.info("create upstream conf {0}".format(ssl_vhost_tmp_file.format(site.name)))
            file_list.append(ssl_vhost_tmp_file.format(site.name))
        else:
            logger.info("create upstream conf {0}".format(vhost_tmp_file.format(site.name)))
            file_list.append(vhost_tmp_file.format(site.name))

        new_content=''
        for m in file_list:
            new_content=new_content+"\r\n####%s####\r\n%s\r\n" %(m,get_file_content(m))

        response = render(req, 'api/conf.html', {"username": req.user.last_name,
                                                   "active": "nginx",
                                                   "conf": new_content,
                                                    "site": site.name,
                                                    "site_id": site_id
                                                   }
                          )
    else:
        response = redirect('login')
    return response

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
            return self.model.objects.filter(mark=name)
        else:
            return self.model.objects.all()

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
            for m in Site_context.objects.filter(site=mission.site):
                m.upstream.status=Status.objects.get(name='online')
                m.upstream.save()

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
            return self.model.objects.filter(name__icontains=name).order_by("-modified_date")
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