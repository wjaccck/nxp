from django.db import models
from rest_framework import serializers


class CommonHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source="%(app_label)s_%(class)s_creator.username")
    last_modified_by = serializers.ReadOnlyField(source="%(app_label)s_%(class)s_last_modified_by.username")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
