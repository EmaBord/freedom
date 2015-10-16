#serializers.py
from models import *
from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer,HyperlinkedRelatedField


class DeviceSerializer(HyperlinkedModelSerializer):
	class Meta:
		model = Device
		fields = ("url","path","created")


class SensorSerializer(HyperlinkedModelSerializer):
	class Meta:
		model = Sensor
		fields = ("url","name","pin","device")

class ActuatorArduinoSerializer(HyperlinkedModelSerializer):
	class Meta:
		model = ActuatorArduino
		fields = ("url","name","pin","device")

class ControllerOnlySensorSerializer(ModelSerializer):
	class Meta:
		model = ControllerOnlySensor
		fields = ("url","name","sensor")

class ControllerOnlyActuatorSerializer(ModelSerializer):
	class Meta:
		model = ControllerOnlyActuator
		fields = ("url","name","actuator")
class ControllerCompleteSerializer(ModelSerializer):
	class Meta:
		model = ControllerComplete
		fields = ("url","name","actuator","sensor","condition","value")

class ValueSerializer(HyperlinkedModelSerializer):
	class Meta:
		model = Value
		fields = ("url","created_hour","created_date","data","sensor")