#coding=utf-8
# Create your views here.
from core.common import logger,get_result
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
import json
from vanilla import ListView, CreateView, UpdateView,DeleteView
from rest_framework.views import APIView
from rest_framework import permissions
from datetime import datetime

class Base_ListViewSet(ListView):

    def get_context_data(self, **kwargs):
        context = super(Base_ListViewSet, self).get_context_data(**kwargs)
        context['create'] = u'创建'
        context['btnsubmit'] = u'提交'
        context['btncancel'] = u'取消'
        context['item']=self.model.verbose()
        context['username']=self.request.user.last_name
        context['is_superuser']=self.request.user.is_superuser
        context['active']=self.model.father()
        return context

class Base_CreateViewSet(CreateView):

    def get_context_data(self, **kwargs):
        context = super(Base_CreateViewSet, self).get_context_data(**kwargs)
        context['create'] = u'创建'
        context['btnsubmit'] = u'提交'
        context['btncancel'] = u'取消'
        context['item']=self.model.verbose()
        context['username']=self.request.user.last_name
        context['is_superuser']=self.request.user.is_superuser
        context['active']=self.model.father()
        return context

class Base_UpdateViewSet(UpdateView):

    def get_context_data(self, **kwargs):
        context = super(Base_UpdateViewSet, self).get_context_data(**kwargs)
        context['create'] = u'创建'
        context['btnsubmit'] = u'提交'
        context['btncancel'] = u'取消'
        context['item']=self.model.verbose()
        context['username']=self.request.user.last_name
        context['is_superuser']=self.request.user.is_superuser
        context['active']=self.model.father()
        return context

class Base_DeleteViewSet(DeleteView):

    def get_context_data(self, **kwargs):
        context = super(Base_DeleteViewSet, self).get_context_data(**kwargs)
        context['title'] = u'删除'
        context['delete_confirmation'] = u'确实删除么'
        context['btnsubmit'] = u'提交'
        context['btncancel'] = u'取消'
        context['item']=self.model.verbose()
        context['username']=self.request.user.last_name
        context['is_superuser']=self.request.user.is_superuser
        context['active'] = self.model.father()
        return context



def format_response(result):
    logger.info('result: %s' % result)
    if result:
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps(get_result(1, 'error request')))

class BaseViewAdmin(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated,)

    def init(self, request):
        pass

    def run(self):
        pass

    def post(self, request, *args, **kwargs):
        self.init(request)
        return format_response(self.run())

    def get(self, request, *args, **kwargs):
        return self.post(request)