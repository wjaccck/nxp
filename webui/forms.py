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

#
# class ProjectForm(forms.ModelForm):
#     name = forms.CharField(label='name', max_length=50, widget=forms.TextInput({'class': 'form-control'}))
#     type = forms.ChoiceField(label='类型',choices=[
#         ('node','node'),
#         ('php','php'),
#         ('java', 'java')
#     ])
#     deploy_dir=forms.CharField(label='部署目录', max_length=100, widget=forms.TextInput({'class': 'form-control'}))
#     git_url=forms.CharField(label='git地址', max_length=100, widget=forms.TextInput({'class': 'form-control'}))
#
#     class Meta:
#         fields = (
#             'name',
#             'type',
#             'deploy_dir',
#             'git_url',
#             'host_list',
#         )
#         model = Project
#         widgets = {
#             'host_list':IpsModelSelect2MultipleWidget,
#         }
#         exclude = ['created_date', 'modified_date']
#
# class MissionFrom(forms.ModelForm):
#     chandao_id = forms.CharField(label=u'禅道ID',
#                               required=True,
#                               max_length=100,
#                               help_text=u'如为最新GIT版本无需填写',
#                               widget=forms.TextInput({'class': 'form-control'}))
#     version = forms.CharField(label=u'版本号',
#                               required=False,
#                               max_length=100,
#                               help_text=u'版本号',
#                               widget=forms.TextInput({'class': 'form-control'}))
#     commit_id = forms.CharField(label='git commit-id',
#                               required=True,
#                               max_length=100,
#                               help_text=u'提交版本号，默认为release版本',
#                               widget=forms.TextInput({'class': 'form-control'}))
#
#     def save(self, commit=True):
#         instance = super(MissionFrom, self).save(commit=False)
#         instance.status=Status.objects.get(name='undo')
#         return instance.save()
#
#     class Meta:
#         fields = (
#             'project',
#             'chandao_id',
#             'version',
#             'commit_id'
#         )
#         model = Mission
#         widgets = {
#             'project':ProjectModelSelect2Widget,
#         }
#         exclude = ['result','status','created_date', 'modified_date']
# #
# # class Item_infoForm(forms.ModelForm):
# #     item = forms.CharField(label='项目名称', max_length=50, widget=forms.TextInput({'class': 'form-control'}))
# #     type = forms.ChoiceField(label='类型',choices=[
# #         ('node','node'),
# #         ('php','php'),
# #         ('java', 'java')
# #     ])
# #     deploy_dir=forms.CharField(label='部署目录', max_length=100, widget=forms.TextInput({'class': 'form-control'}))
# #     git_url=forms.CharField(label='git地址', max_length=100, widget=forms.TextInput({'class': 'form-control'}))
# #     git_location=forms.CharField(label='git本地位置', max_length=100, widget=forms.TextInput({'class': 'form-control'}))
# #     class Meta:
# #         fields = (
# #             'item',
# #             'type',
# #             'deploy_dir',
# #             'git_url',
# #             'git_location',
# #             'hosts',
# #         )
# #         model = Item_info
# #         widgets = {
# #             'hosts':IpsModelSelect2MultipleWidget,
# #         }
# #         exclude = ['created_date', 'modified_date']
# #
# #
# # class PublishForm(forms.ModelForm):
# #     name=forms.CharField(label='版本号', max_length=100, widget=forms.TextInput({'class': 'form-control'}))
# #     git_mark=forms.CharField(label='git-ID', max_length=100, widget=forms.TextInput({'class': 'form-control'}))
# #
# #     def __init__(self, *args, **kwargs):
# #         self.creator = kwargs.pop('creator', None)
# #         self.last_modified_by = kwargs.pop('last_modified_by', None)
# #         super(PublishForm, self).__init__(*args, **kwargs)
# #
# #     def save(self, commit=True):
# #         instance = super(PublishForm, self).save(commit=False)
# #         if self.creator:
# #             instance.creator = self.creator
# #         if self.last_modified_by:
# #             instance.last_modified_by = self.last_modified_by
# #         return instance.save()
# #     class Meta:
# #         fields = (
# #             'name',
# #             'item',
# #             'git_mark',
# #         )
# #         model = Publish
# #         widgets = {
# #             'item':ItemModelSelect2Widget,
# #         }
# #         exclude = ['created_date', 'modified_date','creator','last_modified_by']
