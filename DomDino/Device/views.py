from django.shortcuts import render
from serializers import *
from models import *
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.http import HttpResponse
from arduino import Arduino
import time, json, ast,threading
from rest_framework import filters
from rest_framework.decorators import *
from rest_framework.renderers import *
import pickle

RUN_TASK = False
DELAY_DB_UPDATE = 300 # seconds
DELAY_VERIFY = 0.5 #seconds
DEVICES = []
PATHS = []
SENSOR_ELECTRICITY = 0
ALL = {}
SEM = threading.Semaphore(1)
SEM2 = threading.Semaphore(1)
def P(sem): sem.acquire()
def V(sem):sem.release()

def save(data):
	global SEM2
	P(SEM2)
	arch = open( "/tmp/data", "wb" )
	pickle.dump( data,  arch)
	arch.close()
	V(SEM2)

def read():
	global SEM2
	P(SEM2)
	arch = open( "/tmp/data", "rb" )	
	data =  pickle.load(arch)
	arch.close()
	V(SEM2)
	return data

def update_db(DATA):
	try:
		#DATA = read()
		if DATA:		
			sensors = Sensor.objects.all()
			for sensor in sensors:				
				try:	
					val = DATA[sensor.device.path][sensor.pin]
					value = Value(data = val, sensor = sensor)
					value.save()				
				except:
					try:
						val = DATA[sensor.device.path][sensor.pin]
						value = Value(data = val, sensor = sensor)
						value.save()
					except:
						pass					
	except:
		pass	
		#time.sleep(DELAY_DB_UPDATE)
			
	
def verify():
	global PATHS, DEVICES, SEM,SEM2,ALL
	tiempo = 0
	
	while 1:		
		data = {}
		devices = Device.objects.all()
		for device in devices:
			if device.path not in PATHS:
				PATHS.append(device.path)
				arduino = Arduino(device.path)
				DEVICES.append(arduino)
				
			else:
			
				for dev in DEVICES:
					if dev.getLocation() == device.path:
						arduino = dev
						break
			test = True
			while test:
				#print "while"
				#print 
				try:
					data[device.path] = ast.literal_eval(arduino.readAll())		
					test = False
				except:				
					pass
		controllersComplete = ControllerComplete.objects.all()
		for controller in controllersComplete:
			
			value = ""
			try:
				value = data[controller.sensor.device.path][controller.sensor.pin]

			except Exception,e:
				print e
			try:
				flag = eval(str(value)+controller.condition+controller.value)	
				if controller.actuator.ejecute and not flag:
					P(SEM)
					arduino = Arduino(controller.actuator.device.path)
					ActuatorArduino.objects.filter(id = controller.actuator.id).update(ejecute = False)
					arduino.digitalWriteDown(controller.actuator.pin)
					V(SEM)
			
				elif flag and not controller.actuator.ejecute:
					P(SEM)
					arduino = Arduino(controller.actuator.device.path)
					ActuatorArduino.objects.filter(id = controller.actuator.id).update(ejecute = True)
					arduino.digitalWriteUp(controller.actuator.pin)
					V(SEM)
			except Exception, e:
				print e
		tiempo = tiempo +1
		if tiempo % 40 == 0 or tiempo == 1:
			#print data
			sensors = Sensor.objects.all()
			for sensor in sensors:				
				try:	
					val = data[sensor.device.path][sensor.pin]
					value = Value(data = val, sensor = sensor)
					value.save()				
				except:
					try:
						val = data[sensor.device.path][sensor.pin]
						value = Value(data = val, sensor = sensor)
						value.save()
					except:
						pass
			tiempo = 0
			
		time.sleep(DELAY_VERIFY)	

@api_view(['GET'])
@renderer_classes(( JSONRenderer,))
def run_task(request):
	global RUN_TASK
	if not RUN_TASK:
		import threading
		t1 = threading.Thread(target=verify)
		t1.start()
		print "starts threads!!!"

		RUN_TASK = True
	return Response(json.dumps({"state":"running"}), content_type="application/json")	


@api_view(['GET'])
@renderer_classes(( JSONRenderer,))
def values_date(request,pk,created_date):
	sensor = Sensor.objects.filter(id = pk)[0]
	values = Value.objects.filter(sensor=sensor,created_date = created_date)
	values_filter = []
	total = len(values)/900
	if total != 0:
		for i in range(0,len(values),total):		
				values_filter.append(values[i])
	return Response([{"name":sensor.name,"values":[{"value":value.data,"created_hour":value.created_hour} for value in values_filter]}])

#@api_view(['GET'])
#@renderer_classes(( JSONRenderer,))


def sensor_all(request):
	global ALL
	data = read()
	
	sensors = Sensor.objects.all()
	response = [{"sensors":[]}]
	for sensor in sensors:

		try:
			response[0]["sensors"].append(	{
				"name" : sensor.name,
				"value":ALL[sensor.device.path][sensor.pin]
				})
		except:
			print "utilizando el sensor:",sensor.name," en dispositivo:",sensor.device.path, " siendo su pin:",sensor.pin
		
	return HttpResponse(response)


class DeviceViewSet(ModelViewSet):
	queryset	 = 	Device.objects.all()
	serializer_class =	DeviceSerializer


class SensorViewSet(ModelViewSet):
	queryset	 = 	Sensor.objects.all()
	serializer_class = 	SensorSerializer


	@detail_route()
	def values(self, request,pk):
		sensor = self.get_object()
		values = Value.objects.filter(sensor=sensor)
		return Response([{"name":sensor.name,"values":[{"value":value.data,"created_date":value.created_date,"created_hour":value.created_hour} for value in values]}])

	
		
	@detail_route()
	def read(self, request,pk):
		sensor = self.get_object()
		value = Value.objects.filter(sensor = sensor)
		value = value[len(value)-1]
		return Response([{"sensor_name":sensor.name,"data":value.data,"dc":value.created_date,"hc":value.created_hour}])
	
		
class ActuatorArduinoViewSet(ModelViewSet):
	queryset	 = 	ActuatorArduino.objects.all()
	serializer_class = 	ActuatorArduinoSerializer

	@detail_route()
	def action(self, request,pk):
		global DEVICES,PATHS,SEMAPHORES
		actuator = self.get_object()
		arduino = Arduino(actuator.device.path)
		if actuator.ejecute:
			P(SEM)
			ejecute = False			
			ActuatorArduino.objects.filter(id = actuator.id).update(ejecute = False)
			arduino.digitalWriteDown(actuator.pin)
			V(SEM)
		else:
			P(SEM)
			ejecute = True			
			ActuatorArduino.objects.filter(id = actuator.id).update(ejecute = True)
			arduino.digitalWriteUp(actuator.pin)
			V(SEM)
		return Response([{"actuator_name":actuator.name,"ejecute":ejecute}])

	@detail_route()
	def state(self, request,pk):		
		actuator = self.get_object()
		return Response([{"actuator_name":actuator.name,"state":actuator.ejecute}])
	




class ControllerOnlySensorViewSet(ModelViewSet):
	queryset	 = 	ControllerOnlySensor.objects.all()
	serializer_class = 	ControllerOnlySensorSerializer

class ControllerOnlyActuatorViewSet(ModelViewSet):
	queryset	 = 	ControllerOnlyActuator.objects.all()
	serializer_class = 	ControllerOnlyActuatorSerializer


class ValueViewSet(ModelViewSet):
	queryset	 = 	Value.objects.all()
	serializer_class = 	ValueSerializer

class ControllerCompleteViewSet(ModelViewSet):
	queryset	 = 	ControllerComplete.objects.all()
	serializer_class = 	ControllerCompleteSerializer