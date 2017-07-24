"""nxp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views
from django.conf import settings
if settings.DEBUG:
    import debug_toolbar

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'xadmin/', include(xadmin.site.urls)),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^api/token/', views.obtain_auth_token),
    url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('api.urls')),
    url(r'^swagger/', schema_view),
    url(r'^', include('webui.urls')),
    # url(r'^login/$','django_cas_ng.views.login',name='login'),
    # url(r'^logout/$','django_cas_ng.views.logout',{'next_page': '/',},name='logout'),
]
