# encoding: utf8

from django.db.models import Count
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from .models import *
from .serializers import *
# from rest_framework_filters.backends import DjangoFilterBackend

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