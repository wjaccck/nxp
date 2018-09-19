from django.conf.urls import include, url
# from django.contrib import admin
from webui import views
from webui.forms import LoginForm
from proc.views import Process_ViewSet
# from info_api.models import List
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login,logout

urlpatterns = [
    url(r'^$',views.IndexTemplateView.as_view(),name='index'),
    ### procs
    url(r'^proc/$', Process_ViewSet.as_view(),name='procs'),
    url(r'^proc-list/$', views.Historyprocs_ListViewSet.as_view(), name='procs-list'),

    ### status
    url(r'^status/$',views.Status_ListViewSet.as_view(),name='status-list'),
    url(r'^status/update/(?P<pk>\d+)/$',views.Status_UpdateViewSet.as_view(),name='status-update'),
    url(r'^status/create/$',views.Status_CreateViewSet.as_view(),name='status-create'),

    ### apps-group
    url(r'^apps/$', views.Apps_ListViewSet.as_view(), name='apps-list'),
    url(r'^apps/update/(?P<pk>\d+)/$', views.Apps_UpdateViewSet.as_view(), name='apps-update'),
    url(r'^apps/create/$', views.Apps_CreateViewSet.as_view(), name='apps-create'),

    ### apps-group
    url(r'^apps-group/$', views.Apps_group_ListViewSet.as_view(), name='apps-group-list'),
    url(r'^apps-group/update/(?P<pk>\d+)/$', views.Apps_group_UpdateViewSet.as_view(), name='apps-group-update'),
    url(r'^apps-group/create/$', views.Apps_group_CreateViewSet.as_view(), name='apps-group-create'),

    ### group
    url(r'^group/$', views.Group_ListViewSet.as_view(), name='group-list'),
    url(r'^group/update/(?P<pk>\d+)/$', views.Group_UpdateViewSet.as_view(), name='group-update'),
    url(r'^group/create/$', views.Group_CreateViewSet.as_view(), name='group-create'),

    ### site
    url(r'^site/$', views.Site_ListViewSet.as_view(), name='site-list'),
    url(r'^site/update/(?P<pk>\d+)/$', views.Site_UpdateViewSet.as_view(), name='site-update'),
    url(r'^site/create/$', views.Site_CreateViewSet.as_view(), name='site-create'),
    url(r'^site/delete/(?P<pk>\d+)/$', views.Site_DeleteViewSet.as_view(), name='site-delete'),

    ### site headers
    url(r'^site-headers/$', views.Site_headers_ListViewSet.as_view(), name='site-headers-list'),
    url(r'^site-headers/update/(?P<pk>\d+)/$', views.Site_headers_UpdateViewSet.as_view(), name='site-headers-update'),
    url(r'^site-headers/create/$', views.Site_headers_CreateViewSet.as_view(), name='site-headers-create'),
    url(r'^site-headers/delete/(?P<pk>\d+)/$', views.Site_headers_DeleteViewSet.as_view(), name='site-headers-delete'),

    ### proxy headers
    url(r'^proxy-headers/$', views.Proxy_headers_ListViewSet.as_view(), name='proxy-headers-list'),
    url(r'^proxy-headers/update/(?P<pk>\d+)/$', views.Proxy_headers_UpdateViewSet.as_view(),
        name='proxy-headers-update'),
    url(r'^proxy-headers/create/$', views.Proxy_headers_CreateViewSet.as_view(),
        name='proxy-headers-create'),
    url(r'^proxy-headers/delete/(?P<pk>\d+)/$', views.Proxy_headers_DeleteViewSet.as_view(),
        name='proxy-headers-delete'),

    ### upstream
    url(r'^upstream/$', views.Upstream_ListViewSet.as_view(), name='upstream-list'),
    url(r'^upstream/update/(?P<pk>\d+)/$', views.Upstream_UpdateViewSet.as_view(), name='upstream-update'),
    url(r'^upstream/create/$', views.Upstream_CreateViewSet.as_view(), name='upstream-create'),
    url(r'^upstream/delete/(?P<pk>\d+)/$', views.Upstream_DeleteViewSet.as_view(), name='upstream-delete'),

    ### redis-instance
    url(r'^redis-instance/$', views.Redis_instance_ListViewSet.as_view(), name='redis-instance-list'),
    url(r'^redis-instance/update/(?P<pk>\d+)/$', views.Redis_instance_UpdateViewSet.as_view(),
        name='redis-instance-update'),
    url(r'^redis-instance/create/$', views.Redis_instance_CreateViewSet.as_view(), name='redis-instance-create'),
    url(r'^redis-instance/delete/(?P<pk>\d+)/$', views.Redis_instance_DeleteViewSet.as_view(),
        name='redis-instance-delete'),

    ### redis-group
    url(r'^redis-group/$', views.Redis_group_ListViewSet.as_view(), name='redis-group-list'),
    url(r'^redis-group/update/(?P<pk>\d+)/$', views.Redis_group_UpdateViewSet.as_view(),
        name='redis-group-update'),
    url(r'^redis-group/create/$', views.Redis_group_CreateViewSet.as_view(), name='redis-group-create'),
    url(r'^redis-group/delete/(?P<pk>\d+)/$', views.Redis_group_DeleteViewSet.as_view(),
        name='redis-group-delete'),

    ### codis
    url(r'^codis/$', views.Codis_ListViewSet.as_view(), name='codis-list'),
    url(r'^codis/update/(?P<pk>\d+)/$', views.Codis_UpdateViewSet.as_view(),
        name='codis-update'),
    url(r'^codis/create/$', views.Codis_CreateViewSet.as_view(), name='codis-create'),
    url(r'^codis/delete/(?P<pk>\d+)/$', views.Codis_DeleteViewSet.as_view(),
        name='codis-delete'),

    ### redis-task
    url(r'^redis-task/$', views.Redis_tas_ListViewSet.as_view(), name='redis-task-list'),
    url(r'^redis-task/create/$', views.Redis_task_CreateViewSet.as_view(), name='redis-task-create'),
    url(r'^redis-task-run/(?P<redis_task_id>\d+)/$', views.Run_redis_taskView.as_view(), name='run-redis-task'),

    ### sentinel
    url(r'^sentinel/$', views.Sentinel_ListViewSet.as_view(), name='sentinel-list'),

    ### context
    url(r'^context/$', views.Site_context_ListViewSet.as_view(), name='context-list'),
    url(r'^context/update/(?P<pk>\d+)/$', views.Site_context_UpdateViewSet.as_view(),
        name='context-update'),
    url(r'^context/create/$', views.Site_context_CreateViewSet.as_view(), name='context-create'),
    url(r'^context/delete/(?P<pk>\d+)/$', views.Site_context_DeleteViewSet.as_view(),
        name='context-delete'),

    # ### publish
    url(r'^fun/$', views.Fun_queryTemplate.as_view(), name='fun-query'),
    url(r'^mission/$', views.Tran_missionViewSet.as_view(), name='mission-list'),
    url(r'^create-mission/(?P<site_id>\d+)/$', views.Create_tran_mission.as_view(), name='create-mission'),
    url(r'^create-upstream-mission/(?P<upstream_id>\d+)/$', views.Create_upstream_tran_mission.as_view(), name='create-upstream-mission'),
    #
    url(r'^detail/(?P<site_id>\d+)/$', views.Get_detailTemplate.as_view(), name='get-detail'),
    url(r'^upstream-detail/(?P<upstream_id>\d+)/$', views.Get_upstream_detailTemplate.as_view(), name='get-upstream-detail'),
    url(r'^codis-detail/(?P<codis_id>\d+)/$', views.Codis_detailTemplate.as_view(), name='get-codis-detail'),
    url(r'^sentinel-detail/(?P<sentinel_id>\d+)/$', views.Sentinel_detailTemplate.as_view(), name='get-sentinel-detail'),
    url(r'^query-redis/$', views.Codis_queryTemplate.as_view(), name='query-redis'),

    url(r'^conf/(?P<site_id>\d+)/$', views.Generate_vhostTemplate.as_view(), name='get-conf'),
    url(r'^upstream-conf/(?P<upstream_id>\d+)/$', views.Generate_upstream_confTemplate.as_view(), name='get-upstream-conf'),

    url(r'^check-conf/(?P<site_id>\d+)/$', views.Check_confTemplate.as_view(), name='check-conf'),
    url(r'^upstream-check-conf/(?P<upstream_id>\d+)/$', views.Check_upstreamTemplate.as_view(), name='check-upstream-conf'),
    url(r'^run/(?P<mission_id>\d+)/$', login_required(views.Run_mission), name='run-mission'),
    # #
    # url(r'^reset/(?P<job_id>\d+)/$', login_required(views.reset_job), name='reset-job'),
    url(r'^request-count/$', views.Http_request_countTemplate.as_view(), name='request-count'),
    url(r'^request-statistics/$', views.Http_request_statisticsTemplate.as_view(), name='request-statistics'),

    url(r'^login/$',
        login,
        {
            'template_name': 'webui/login.html',
            'authentication_form': LoginForm,

        },
        name='login',),

    # Django Select2
    url(r'^select2/', include('django_select2.urls')),

    url(r'^logout/$',
        logout,
        {
            'next_page': '/',
        },
        name='logout'),]
