# encoding: utf8
from rest_framework import routers
from api import views

# router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()

router.register(r'ipv4address', views.Ipv4Address_ApiViewSet)
router.register(r'ipv4network', views.Ipv4Network_ApiViewSet)
router.register(r'codis', views.Codis_ApiViewSet)

urlpatterns = router.urls