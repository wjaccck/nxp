# encoding: utf8
from rest_framework import serializers
from netaddr import *
from abstract.serializers import CommonHyperlinkedModelSerializer
from .models import *


class IPv4AddressSerializer(CommonHyperlinkedModelSerializer):

    class Meta:
        model = Ipv4Address
        fields = '__all__'

class IPv4NetworkSerializer(CommonHyperlinkedModelSerializer): 


    class Meta:
        model = Ipv4Network
        fields = '__all__'

    def create(self, validated_data):
        prefix = validated_data['name']
        nwk = IPNetwork(prefix)        
        rawAddrs = [Ipv4Address(name=str(x), creator=validated_data['creator'], \
                    last_modified_by=validated_data['last_modified_by']) for x in list(nwk)]
        addresses = Ipv4Address.objects.bulk_create(rawAddrs, batch_size=30)
        return super(IPv4NetworkSerializer, self).create(validated_data)

    def validate(self, attrs):
        if attrs['name'].find('/') == -1:
            raise serializers.ValidationError('Network mask is missing!')

        return super(IPv4NetworkSerializer, self).validate(attrs)


class CodisSerializer(serializers.HyperlinkedModelSerializer):
    member=serializers.SlugRelatedField(queryset=Redis_group.objects.all(), many=True,slug_field='name')
    detail=serializers.SerializerMethodField()
    class Meta:
        model = Codis
        fields='__all__'

    def get_detail(self,obj):
        groups=obj.member.all()
        result=[]
        for m in groups:
            t_result={}
            t_result[m.name]={"master":m.master.__str__(),"slave":[y.__str__() for y in m.slave.all()]}
            result.append(t_result)
        # return [{"x":{"master":x.master,"slave":x.slave.all(),"offline":x.offline.all()}} for x in groups]
        return result