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
            t_result['name']=m.name
            t_result['master']=m.master.__str__()
            t_result['slave']=[x.__str__() for x in m.slave.all()]
            t_result['offline']=[x.__str__() for x in m.offline.all()]
            result.append(t_result)
        # return [{"x":{"master":x.master,"slave":x.slave.all(),"offline":x.offline.all()}} for x in groups]
        return result

class SentinelSerializer(serializers.HyperlinkedModelSerializer):
    member=serializers.SlugRelatedField(queryset=Redis_group.objects.all(), many=True,slug_field='name')
    detail=serializers.SerializerMethodField()
    class Meta:
        model = Sentinel
        fields='__all__'

    def get_detail(self,obj):
        groups=obj.member.all()
        result=[]
        for m in groups:
            t_result={}
            t_result['name']=m.name
            t_result['master']=m.master.__str__()
            t_result['slave']=[x.__str__() for x in m.slave.all()]
            t_result['offline']=[x.__str__() for x in m.offline.all()]
            result.append(t_result)
        # return [{"x":{"master":x.master,"slave":x.slave.all(),"offline":x.offline.all()}} for x in groups]
        return result


# class Site(CommonModel,NGINX_BASE):
#     name=models.CharField(max_length=50)
#     group=models.ForeignKey(Group,related_name='site_group')
#     https=models.BooleanField()

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    group=serializers.SlugRelatedField(queryset=Group.objects.all(), many=False,slug_field='name')
    detail=serializers.SerializerMethodField()
    class Meta:
        model = Site
        fields='__all__'

    def get_detail(self,obj):
        all_context=Site_context.objects.filter(site=obj)
        result=[]
        for m in all_context:
            t_result={}
            t_result['upstream']=m.upstream.name
            t_result['context']=m.context
            if m.upstream.direct_status:
                t_result['app_info']=[]
            else:
                t_result['app_info']=[x.__str__() for x in m.upstream.docker_list.all()]+["{0}:{1}".format(x,m.upstream.port) for x in m.upstream.hosts.all()]
            result.append(t_result)
        # return [{"x":{"master":x.master,"slave":x.slave.all(),"offline":x.offline.all()}} for x in groups]
        return result