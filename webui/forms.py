# #coding=utf8
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from api.models import *
from .wiget import *

class LoginForm(AuthenticationForm):
    '''Authentication form which uses boostrap CSS.'''
    username = forms.CharField(max_length=255,widget=forms.TextInput({
                                   'class': 'form-control'}))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput({
                                   'class': 'form-control'}))


class StatusForm(forms.ModelForm):

    name = forms.CharField(label='名字', max_length=50, widget=forms.TextInput({'class': 'form-control'}))

    class Meta:
        model = Status
        exclude = ['created_date', 'modified_date']


class Nginx_groupForm(forms.ModelForm):

    name = forms.CharField(label='名字', max_length=50, widget=forms.TextInput({'class': 'form-control'}))

    class Meta:
        fields = (
                    'name',
                    'hosts',
                )
        model = Nginx_group
        widgets = {
            'hosts':ModelSelect2MultipleWidget,
        }
        exclude = ['created_date', 'modified_date']

class AppsForm(forms.ModelForm):

    port = forms.CharField(label='端口', max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    def clean(self):
        cleaned_data = super(AppsForm,self).clean()
        host = cleaned_data.get('host')
        port = cleaned_data.get('port')
        if Apps.objects.filter(host=host,port=port).count()>0:
            self._errors['port'] = self.error_class([u"应用已经录入"])
    class Meta:
        fields = (
                    'host',
                    'port',
                    'status',
                )
        model = Apps
        widgets = {
            'host':ApphostSelect2Widget,
            'status': AppstatusSelect2Widget,
        }
        exclude = ['created_date', 'modified_date']



class Apps_groupForm(forms.ModelForm):

    name = forms.CharField(label='名字', max_length=50, widget=forms.TextInput({'class': 'form-control'}))

    class Meta:
        fields = (
                    'name',
                    'apps',
                )
        model = Apps_group
        widgets = {
            'apps':AppsModelSelect2MultipleWidget,
        }
        exclude = ['created_date', 'modified_date']



class SiteForm(forms.ModelForm):

    name = forms.CharField(label='域名', max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    http = forms.BooleanField(label='是否为http',required=False)
    https = forms.BooleanField(label='是否为https',required=False)
    http2 = forms.BooleanField(label='是否为http2',required=False)
    trace_status = forms.BooleanField(label='是否添加trace-id',required=False)
    redirect_status = forms.BooleanField(label='是否为重定向至https',required=False)
    def clean(self):
        cleaned_data = super(SiteForm,self).clean()
        name = cleaned_data.get('name')
        http = cleaned_data.get('http')
        https = cleaned_data.get('https')
        http2 = cleaned_data.get('http2')
        group = cleaned_data.get('group')
        redirect_status = cleaned_data.get('redirect_status')
        if not any([http,https,http2]):
            self._errors['http'] = self.error_class([u"至少选择监听一个端口"])
        if https and redirect_status:
            self._errors['redirect_status'] = self.error_class([u"不可做http至https的重定向"])
        else:
            if Site.objects.filter(name=name,https=https,group=group).__len__()<2:
                return cleaned_data
            else:
                self._errors['name'] = self.error_class([u"该站点在本组已有配置"])


    class Meta:
        fields = (
            'name',
            'http',
            'https',
            'http2',
            'trace_status',
            'redirect_status',
            'group',
            'extra_parameters',
        )
        widgets = {
            'group':GroupModelSelect2Widget,
            'extra_parameters':SiteheadersSelect2MultipleWidget
        }
        model = Site
        exclude = ['created_date', 'modified_date']

class Site_headersForm(forms.ModelForm):
    name = forms.CharField(label='名称', max_length=20, widget=forms.TextInput({'class': 'form-control'}))
    extra_parameter = forms.CharField(label='站点自定义头', max_length=255, widget=forms.TextInput({'class': 'form-control'}))
    class Meta:
        fields = (
            'name',
            'extra_parameter',
        )
        model = Site_headers
        exclude = ['created_date', 'modified_date']

class Proxy_headersForm(forms.ModelForm):
    name = forms.CharField(label='名称', max_length=20, widget=forms.TextInput({'class': 'form-control'}))
    extra_parameter = forms.CharField(label='Proxy自定义头', max_length=255, widget=forms.TextInput({'class': 'form-control'}))
    class Meta:
        fields = (
            'name',
            'extra_parameter',
        )
        model = Proxy_headers
        exclude = ['created_date', 'modified_date']


class UpstreamForm(forms.ModelForm):
    name = forms.CharField(label='组名', max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    domain_proxy = forms.CharField(label='域名代理', required=False,max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    ip_hash = forms.BooleanField(label='是否为ip_hash', required=False)

    def clean(self):
        cleaned_data = super(UpstreamForm,self).clean()
        domain_proxy = cleaned_data.get('domain_proxy')
        app = cleaned_data.get('app')
        if domain_proxy:
            domain_status=1
        else:
            domain_status=0
        if app:
            app_status=1
        else:
            app_status=0

        upstream_status=domain_status+app_status
        if upstream_status!=1:
            self._errors['app'] = self.error_class([u"只能选择一个代理内容，域名或者app"])
        else:
            return cleaned_data


    def save(self, commit=True):
        instance = super(UpstreamForm, self).save(commit=False)
        instance.status=Status.objects.get(name='undo')
        instance.save()
        # instance.save_m2m()
        return self.save_m2m()

    class Meta:
        fields = (
            'name',
            'domain_proxy',
            'app',
            'status',
            'ip_hash',
            'group'
        )
        widgets = {
            'app': AppModelSelect2Widget,
            'group':Upstream_groupModelSelect2Widget,
        }
        model = Upstream
        exclude = ['created_date', 'modified_date','status']

class Site_contextForm(forms.ModelForm):
    context = forms.CharField(label='context_path', max_length=200, widget=forms.TextInput({'class': 'form-control'}))
    proxy_path = forms.CharField(label='proxy_path', required=False,max_length=200, widget=forms.TextInput({'class': 'form-control'}))

    def save(self, commit=True):
        instance = super(Site_contextForm, self).save(commit=False)
        instance.status = Status.objects.get(name='undo')
        instance.save()
        return self.save_m2m()

    class Meta:
        fields = (
            'site',
            'context',
            'upstream',
            'proxy_path',
            'default_proxy_set',
            'extra_parametres',
        )
        widgets = {
            'site': SiteModelSelect2Widget,
            'upstream': UpstreamSelect2Widget,
            'extra_parametres': ProxyheadersSelect2MultipleWidget,

        }
        model = Site_context
        exclude = ['created_date', 'modified_date', 'status']



class Redis_instanceForm(forms.ModelForm):
    port = forms.CharField(label='端口', required=True,max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    version = forms.CharField(label='版本', required=False, max_length=50, widget=forms.TextInput({'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(Redis_instanceForm,self).clean()
        host = cleaned_data.get('host')
        port = cleaned_data.get('port')
        if Redis_instance.objects.filter(host=host,port=port).__len__()==0:
            return cleaned_data
        else:
            self._errors['port'] = self.error_class([u"该服务器端口已被占用"])

    class Meta:
        fields = (
            'host',
            'port',
            'version',
        )
        widgets = {
            'host': Redis_instanceSelect2Widget,
        }
        model = Redis_instance
        exclude = ['created_date', 'modified_date',]

class Redis_groupForm(forms.ModelForm):
    name = forms.CharField(label='组名', required=True,max_length=50, widget=forms.TextInput({'class': 'form-control'}))

    class Meta:
        fields = (
            'name',
            'master',
            'slave',
            'offline'
        )
        widgets = {
            'master': Redis_instanceSelect2Widget,
            'slave': Redis_instanceMultipleWidget,
            'offline': Redis_instanceMultipleWidget,
        }
        model = Redis_group
        exclude = ['created_date', 'modified_date',]


class CodisForm(forms.ModelForm):
    name = forms.CharField(label='名称', required=True,max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    admin_http = forms.URLField(label='admin地址', required=False,max_length=50, widget=forms.TextInput({'class': 'form-control'}))

    class Meta:
        fields = (
            'name',
            'admin_http',
            'member',
        )
        widgets = {
            'member': Redis_groupMultipleWidget,
        }
        model = Codis
        exclude = ['created_date', 'modified_date',]



# class Docker_appForm(forms.ModelForm):
#     port = forms.CharField(label='端口', required=True,max_length=10, widget=forms.TextInput({'class': 'form-control'}))
#
#     class Meta:
#         fields = (
#             'host',
#             'port',
#         )
#         widgets = {
#             'host': Docker_appSelect2Widget,
#         }
#         model = Docker_app
#         exclude = ['created_date', 'modified_date',]

# class Redis_task(CommonModel,REDIS_BASE):
#     master_ip=models.ForeignKey(Ipv4Address,blank=True)
#     master_port=models.CharField(max_length=10,blank=True)
#     redis_host=models.ForeignKey(Ipv4Address)
#     redis_port=models.CharField(max_length=10)
#     size=models.CharField(max_length=10)
#     result=models.TextField(blank=True)
#     status=models.ForeignKey(Status)

class Redis_taskForm(forms.ModelForm):
    master_port = forms.CharField(label='master端口', required=False,max_length=10, widget=forms.TextInput({'class': 'form-control'}))
    redis_port = forms.CharField(label='实例端口', required=True,max_length=10, widget=forms.TextInput({'class': 'form-control'}))
    size = forms.CharField(label='占用内存', required=True,max_length=10, widget=forms.TextInput({'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(Redis_taskForm,self).clean()
        master_ip = cleaned_data.get('master_ip')
        master_port = cleaned_data.get('master_port')
        redis_ip = cleaned_data.get('redis_ip')
        redis_port = cleaned_data.get('redis_port')
        if Redis_instance.objects.filter(host=redis_ip,port=redis_port).__len__()==0:
            if master_ip and master_port:
                if Redis_instance.objects.filter(host=master_ip,port=master_port).__len__()==0:
                    self._errors['master_ip'] = self.error_class([u"master实例不存在"])
                else:
                    return cleaned_data
            else:
                return cleaned_data
        else:
            self._errors['port'] = self.error_class([u"该服务器端口已被占用"])

    def save(self, commit=True):
        instance = super(Redis_taskForm, self).save(commit=False)
        instance.status = Status.objects.get(name='undo')
        return instance.save()

    class Meta:
        fields = (
            'redis_ip',
            'redis_port',
            'size',
            'master_ip',
            'master_port',
        )
        widgets = {
            'master_ip': Redis_task_masterSelect2Widget,
            'redis_ip': Redis_task_redisSelect2Widget,
        }
        model = Redis_task
        exclude = ['created_date', 'modified_date','status','result']