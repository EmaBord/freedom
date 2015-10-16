from django.db import models

# Create your models here.
class Device(models.Model):
	path 	= models.CharField(max_length = 200)
	created = models.DateTimeField(auto_now_add = True)
	active	= models.BooleanField(default= True)
	def __unicode__(self):return self.path

class Data(models.Model):
	data 	= models.TextField()

class Sensor(models.Model):
	name 	= models.CharField(max_length= 200)
	pin		= models.CharField(max_length=3)
	device	= models.ForeignKey(Device,related_name="sensor")
	def __unicode__(self):return self.name

class Actuator(models.Model):
	name 	= models.CharField(max_length= 200)
	device	= models.ForeignKey(Device,related_name="actuator")
	def __unicode__(self):return self.name	
class ActuatorArduino(Actuator):
	pin		= models.IntegerField()
	ejecute = models.BooleanField(default= False)


class Value(models.Model):
	created_hour = models.TimeField(auto_now_add=True)
	created_date = models.DateField(auto_now_add=True)
	data	= models.CharField(max_length=50)
	sensor  = models.ForeignKey(Sensor, related_name='sensor_data')
		
class Controller(models.Model):
	name 	= models.CharField(max_length= 200)	
	def __unicode__(self):return self.name
	
class ControllerOnlySensor(Controller):
	sensor 	= models.ForeignKey(Sensor, related_name='controller_s')
	
class ControllerComplete(Controller):
	actuator 	= models.ForeignKey(ActuatorArduino, related_name='controller_actuator')
	sensor 	= models.ForeignKey(Sensor, related_name='controller_sensor')
	condition = models.CharField(max_length=1)
	value = models.CharField(max_length=4)
	
class ControllerOnlyActuator(Controller):
	actuator 	= models.ForeignKey(ActuatorArduino, related_name='controller_a')

	
	
