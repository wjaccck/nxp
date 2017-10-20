from django.conf.urls import include, url
# from django.contrib import admin
from webui import views
from webui.forms import LoginForm
# from info_api.models import List
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login,logout

urlpatterns = [
    url(r'^$',views.index,name='index'),
    ### status
    url(r'^status/$',login_required(views.Status_ListViewSet.as_view()),name='status-list'),
    url(r'^status/update/(?P<pk>\d+)/$',login_required(views.Status_UpdateViewSet.as_view()),name='status-update'),
    url(r'^status/create/$',login_required(views.Status_CreateViewSet.as_view()),name='status-create'),

    ### status
    url(r'^group/$', login_required(views.Group_ListViewSet.as_view()), name='group-list'),
    url(r'^group/update/(?P<pk>\d+)/$', login_required(views.Group_UpdateViewSet.as_view()), name='group-update'),
    url(r'^group/create/$', login_required(views.Group_CreateViewSet.as_view()), name='group-create'),

    ### project
    url(r'^site/$', login_required(views.Site_ListViewSet.as_view()), name='site-list'),
    url(r'^site/update/(?P<pk>\d+)/$', login_required(views.Site_UpdateViewSet.as_view()), name='site-update'),
    url(r'^site/create/$', login_required(views.Site_CreateViewSet.as_view()), name='site-create'),
    url(r'^site/delete/(?P<pk>\d+)/$', login_required(views.Site_DeleteViewSet.as_view()), name='site-delete'),

    ### upstream
    url(r'^upstream/$', login_required(views.Upstream_ListViewSet.as_view()), name='upstream-list'),
    url(r'^upstream/update/(?P<pk>\d+)/$', login_required(views.Upstream_UpdateViewSet.as_view()), name='upstream-update'),
    url(r'^upstream/create/$', login_required(views.Upstream_CreateViewSet.as_view()), name='upstream-create'),
    url(r'^upstream/delete/(?P<pk>\d+)/$', login_required(views.Upstream_DeleteViewSet.as_view()), name='upstream-delete'),

    ### redis-instance
    url(r'^redis-instance/$', login_required(views.Redis_instance_ListViewSet.as_view()), name='redis-instance-list'),
    url(r'^redis-instance/update/(?P<pk>\d+)/$', login_required(views.Redis_instance_UpdateViewSet.as_view()),
        name='redis-instance-update'),
    url(r'^redis-instance/create/$', login_required(views.Redis_instance_CreateViewSet.as_view()), name='redis-instance-create'),
    url(r'^redis-instance/delete/(?P<pk>\d+)/$', login_required(views.Redis_instance_DeleteViewSet.as_view()),
        name='redis-instance-delete'),

    ### redis-group
    url(r'^redis-group/$', login_required(views.Redis_group_ListViewSet.as_view()), name='redis-group-list'),
    url(r'^redis-group/update/(?P<pk>\d+)/$', login_required(views.Redis_group_UpdateViewSet.as_view()),
        name='redis-group-update'),
    url(r'^redis-group/create/$', login_required(views.Redis_group_CreateViewSet.as_view()), name='redis-group-create'),
    url(r'^redis-group/delete/(?P<pk>\d+)/$', login_required(views.Redis_group_DeleteViewSet.as_view()),
        name='redis-group-delete'),

    ### codis
    url(r'^codis/$', login_required(views.Codis_ListViewSet.as_view()), name='codis-list'),
    url(r'^codis/update/(?P<pk>\d+)/$', login_required(views.Codis_UpdateViewSet.as_view()),
        name='codis-update'),
    url(r'^codis/create/$', login_required(views.Codis_CreateViewSet.as_view()), name='codis-create'),
    url(r'^codis/delete/(?P<pk>\d+)/$', login_required(views.Codis_DeleteViewSet.as_view()),
        name='codis-delete'),

    ### docker
    url(r'^docker/$', login_required(views.Docker_app_ListViewSet.as_view()), name='docker-list'),
    url(r'^docker/update/(?P<pk>\d+)/$', login_required(views.Docker_app_UpdateViewSet.as_view()),
        name='codis-update'),
    url(r'^docker/create/$', login_required(views.Docker_app_CreateViewSet.as_view()), name='docker-create'),
    url(r'^docker/delete/(?P<pk>\d+)/$', login_required(views.Docker_app_DeleteViewSet.as_view()),
        name='docker-delete'),

    ### redis-task
    url(r'^redis-task/$', login_required(views.Redis_tas_ListViewSet.as_view()), name='redis-task-list'),
    url(r'^redis-task/create/$', login_required(views.Redis_task_CreateViewSet.as_view()), name='redis-task-create'),
    url(r'^redis-task-run/(?P<redis_task_id>\d+)/$', login_required(views.Run_redis_task), name='run-redis-task'),

    ### sentinel
    url(r'^sentinel/$', login_required(views.Sentinel_ListViewSet.as_view()), name='sentinel-list'),
    # url(r'^codis/update/(?P<pk>\d+)/$', login_required(views.Codis_UpdateViewSet.as_view()),
    #     name='codis-update'),
    # url(r'^codis/create/$', login_required(views.Codis_CreateViewSet.as_view()), name='codis-create'),
    # url(r'^codis/delete/(?P<pk>\d+)/$', login_required(views.Codis_DeleteViewSet.as_view()),
    #     name='codis-delete'),

    ### context
    url(r'^context/$', login_required(views.Site_context_ListViewSet.as_view()), name='context-list'),
    url(r'^context/update/(?P<pk>\d+)/$', login_required(views.Site_context_UpdateViewSet.as_view()),
        name='context-update'),
    url(r'^context/create/$', login_required(views.Site_context_CreateViewSet.as_view()), name='context-create'),
    url(r'^context/delete/(?P<pk>\d+)/$', login_required(views.Site_context_DeleteViewSet.as_view()),
        name='context-delete'),

    # ### publish
    url(r'^fun/$', login_required(views.Fun_queryView), name='fun-query'),
    url(r'^mission/$', login_required(views.Tran_missionViewSet.as_view()), name='mission-list'),
    url(r'^create-mission/(?P<site_id>\d+)/$', login_required(views.Create_tran_mission), name='create-mission'),
    #
    # ### version
    # url(r'^version/$', login_required(views.Version_historyViewSet.as_view()), name='version-list'),
    # url(r'^progress/$', login_required(views.Progress_ViewSet.as_view()), name='progress-list'),
    # #
    url(r'^detail/(?P<site_id>\d+)/$', login_required(views.Get_detail), name='get-detail'),
    url(r'^codis-detail/(?P<codis_id>\d+)/$', login_required(views.Codis_detailView), name='get-codis-detail'),
    url(r'^sentinel-detail/(?P<sentinel_id>\d+)/$', login_required(views.Sentinel_detailView), name='get-sentinel-detail'),
    url(r'^query-redis/$', login_required(views.Codis_queryView), name='query-redis'),

    url(r'^conf/(?P<site_id>\d+)/$', login_required(views.Generate_conf), name='get-conf'),

    url(r'^check-conf/(?P<site_id>\d+)/$', login_required(views.Conf_check), name='check-conf'),
    url(r'^run/(?P<mission_id>\d+)/$', login_required(views.Run_mission), name='run-mission'),
    # #
    # url(r'^reset/(?P<job_id>\d+)/$', login_required(views.reset_job), name='reset-job'),

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
