# encoding: utf8

from django.db.models import Count
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from .models import *
from .serializers import *
# from rest_framework_filters.backends import DjangoFilterBackend

# class Site_ApiViewSet(viewsets.ModelViewSet):
#     http_method_names = [ 'get']
#     queryset = Site.objects.all()
#     serializer_class = SiteSerializer
#     permission_classes = (permissions.DjangoModelPermissions,)
#     filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
#     filter_fields = ('name',)
#     search_fields = ('^name', )

class Apps_ApiViewSet(viewsets.ModelViewSet):
    http_method_names = [ 'get','post']
    queryset = Apps.objects.all()
    serializer_class = AppsSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('host',)
    search_fields = ('^host', )


class Codis_ApiViewSet(viewsets.ModelViewSet):
    http_method_names = [ 'get','post']
    queryset = Codis.objects.all()
    serializer_class = CodisSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('name',)
    search_fields = ('^name', )

class Sentinel_ApiViewSet(viewsets.ModelViewSet):
    http_method_names = [ 'get','post']
    queryset = Sentinel.objects.all()
    serializer_class = SentinelSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('name',)
    search_fields = ('^name', )

class Request_count_ApiViewSet(viewsets.ModelViewSet):
    http_method_names = [ 'get','post']
    queryset = Http_statistics.objects.all()
    serializer_class = Request_countSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('group','host','daytime','domain')
    search_fields = ('^domain', )

class Ipv4Address_ApiViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    http_method_names = ['get']
    queryset=Ipv4Address.objects.select_related('creator', 'last_modified_by')\
                                .all()
    serializer_class = IPv4AddressSerializer
    # Applies permissions
    permission_classes = (permissions.DjangoModelPermissions,)
    # Applies Filters
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('name',)
    search_fields = ('^name', )
    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        serializer.save(
            creator = self.request.user,
            last_modified_by = self.request.user
        )
        return super(Ipv4Address_ApiViewSet, self).perform_create(serializer)


class Ipv4Network_ApiViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    http_method_names = ['get', 'post']
    queryset=Ipv4Network.objects.select_related('creator', 'last_modified_by')\
                                .all()
    serializer_class = IPv4NetworkSerializer

    # Applies permissions
    permission_classes = (permissions.DjangoModelPermissions,)

    # Applies Filters
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('name', )
    search_fields = ('^name', )

    def perform_create(self, serializer):
        serializer.save(
            creator = self.request.user,
            last_modified_by = self.request.user
        )
        return super(Ipv4Network_ApiViewSet, self).perform_create(serializer)