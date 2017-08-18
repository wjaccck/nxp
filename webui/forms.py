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


class GroupForm(forms.ModelForm):

    name = forms.CharField(label='名字', max_length=50, widget=forms.TextInput({'class': 'form-control'}))

    class Meta:
        fields = (
                    'name',
                    'hosts',
                )
        model = Group
        widgets = {
            'hosts':ModelSelect2MultipleWidget,
        }
        exclude = ['created_date', 'modified_date']



class SiteForm(forms.ModelForm):

    name = forms.CharField(label='域名', max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    https = forms.BooleanField(label='是否为https',required=False)
    class Meta:
        fields = (
            'name',
            'https',
            'group'
        )
        widgets = {
            'group':GroupModelSelect2Widget,
        }
        model = Site
        exclude = ['created_date', 'modified_date']

class UpstreamForm(forms.ModelForm):
    name = forms.CharField(label='组名', max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    port = forms.CharField(label='端口', required=False,max_length=50, widget=forms.TextInput({'class': 'form-control'}))
    direct_status = forms.BooleanField(label='是否为代理域名', required=False)

    def save(self, commit=True):
        instance = super(UpstreamForm, self).save(commit=False)
        instance.status=Status.objects.get(name='undo')
        instance.save()
        # instance.save_m2m()
        return self.save_m2m()

    class Meta:
        fields = (
            'name',
            'port',
            'hosts',
            'direct_status',
        )
        widgets = {
            'hosts': UpstreamModelSelect2MultipleWidget,
        }
        model = Upstream
        exclude = ['created_date', 'modified_date','status']

class Site_contextForm(forms.ModelForm):
    context = forms.CharField(label='context_path', max_length=200, widget=forms.TextInput({'class': 'form-control'}))
    
    def save(self, commit=True):
        instance = super(Site_contextForm, self).save(commit=False)
        instance.status = Status.objects.get(name='undo')
        return instance.save()

    class Meta:
        fields = (
            'site',
            'context',
            'upstream',
            'extra_parametres',
        )
        widgets = {
            'site': SiteModelSelect2Widget,
            'upstream': UpstreamSelect2Widget,
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