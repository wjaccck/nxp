from django import http
import json
# from ansible_api import settings
import sys
from django.views.debug import technical_500_response
from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class WhiteIpMiddleware(MiddlewareMixin):

    def process_request(self, request):
        host=request.META['HTTP_X_REAL_IP']
        if host.startswith('10.') or host.startswith('172.'):
            pass
        else:
        # if request.META['HTTP_X_REAL_IP'] not in getattr(settings, "WHITE_IPS", []):
            return http.HttpResponseForbidden(json.dumps({"msg":" %s forbidden" %host}))




class UserBasedExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('HTTP_X_REAL_IP') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())