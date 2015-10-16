from django.conf.urls import include, url
from django.contrib import admin
from Device.views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'device',DeviceViewSet)
router.register(r'sensor',SensorViewSet)
router.register(r'actuator',ActuatorArduinoViewSet)
router.register(r'controllerOnlySensor',ControllerOnlySensorViewSet)
router.register(r'controllerOnlyActuator',ControllerOnlyActuatorViewSet)
router.register(r'controllerComplete',ControllerCompleteViewSet)
#router.register(r'values',ValueViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include(router.urls)),	
    url(r'^start/',run_task),
    url(r'^sensor/(?P<pk>[^/.]+)/values_date/(?P<created_date>[^/.]+)/',values_date),
    url(r'^sensor_all/',sensor_all),



]