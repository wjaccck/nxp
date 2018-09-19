#coding=utf8
from rest_framework import permissions
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseServerError
import json
from core.common import logger,get_result
from rest_framework.views import APIView
from .models import Machine_procs
from .tasks import Proc_info

class Process_ViewSet(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated,)
    model = Machine_procs
    def post(self, request):
        host = self.request.data.get('host',None)
        procs = self.request.data.get('procs',None)
        if host is None or procs is None:
            response=HttpResponseBadRequest(json.dumps(get_result(1, 'no correct data in the body')))
        else:
            try:
                Proc_info().apply_async(args=(host,procs))
                response=HttpResponse(json.dumps(get_result(0,'add')))
            except Exception as e:
                response=HttpResponseServerError(json.dumps(get_result(1,'add async task failed:{0}'.format(str(e)))))
        return response