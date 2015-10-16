
import serial
class  Arduino():
	def __init__(self,location = None):
		if location:
			self.location = location 
		else:
			try:
				self.location = commands.getoutput("ls /dev/ttyACM*")
				
				if "ls" in self.location:
					self.location = commands.getoutput("ls /dev/ttyUSB*")
				if "ls" in self.location:
					raise(GeneratorExit)	
			except:
				raise(GeneratorExit)
						
		self.serial = serial.Serial(self.location, timeout=2)
	def getLocation(self): return self.location		
	def analogRead(self,pin):
		self.serial.write(str(pin))
		result = self.serial.readline().strip()
		return result
	
	def digitalRead(self,pin):
		if pin == 0: 	pin = "A"
		elif pin == 1:	pin = "B"
		elif pin == 2:	pin = "C"
		elif pin == 3:	pin = "D"
		elif pin == 4:	pin = "E"
		elif pin == 5:	pin = "F"
		elif pin == 6:	pin = "G"
		elif pin == 7:	pin = "H"
		elif pin == 8:	pin = "I"
		elif pin == 9:	pin = "J"
		elif pin == 10:	pin = "K"
		elif pin == 11:	pin = "L"
		elif pin == 12:	pin = "M"
		elif pin == 13:	pin = "N"
		return self.analogRead(pin)
	
	def digitalWriteUp(self,pin):
		if pin == 0: 	pin = "a"
		elif pin == 1:	pin = "b"
		elif pin == 2:	pin = "c"
		elif pin == 3:	pin = "d"
		elif pin == 4:	pin = "e"
		elif pin == 5:	pin = "f"
		elif pin == 6:	pin = "g"
		elif pin == 7:	pin = "h"
		elif pin == 8:	pin = "i"
		elif pin == 9:	pin = "j"
		elif pin == 10:	pin = "k"
		elif pin == 11:	pin = "l"
		elif pin == 12:	pin = "m"
		elif pin == 13:	pin = "n"
		self.serial.write(str(pin))
	
	def digitalWriteDown(self,pin):
		if pin == 0: 	pin = "o"
		elif pin == 1:	pin = "p"
		elif pin == 2:	pin = "q"
		elif pin == 3:	pin = "r"
		elif pin == 4:	pin = "s"
		elif pin == 5:	pin = "t"
		elif pin == 6:	pin = "u"
		elif pin == 7:	pin = "v"
		elif pin == 8:	pin = "w"
		elif pin == 9:	pin = "x"
		elif pin == 10:	pin = "y"
		elif pin == 11:	pin = "z"
		elif pin == 12:	pin = "O"
		elif pin == 13:	pin = "P"
		self.serial.write(str(pin))
	def pulseInUltrasound(self): 
		"""Pin 8-Echo Pin 9-Trig"""
		return self.analogRead("_")
	def pulseIn(self,pin):
		""" parameter number pin will be Echo next number pin will be Trig"""
		if pin == 2: 	pin = "Q"
		elif pin == 3:	pin = "R"
		elif pin == 4:	pin = "S"
		elif pin == 5:	pin = "T"
		elif pin == 6:	pin = "U"
		elif pin == 7:	pin = "V"
		elif pin == 8:	pin = "W"
		elif pin == 9:	pin = "X"
		elif pin == 10:	pin = "Y"
		elif pin == 11:	pin = "Z"
		elif pin == 12:	pin = "{"
		elif pin == 13:	pin = "}"
		return self.analogRead(pin)
	
	def digitalReadDTH(self,pin):
		if pin == 2: 	pin = "!"
		elif pin == 3:	pin = "-"
		elif pin == 4:	pin = "$"
		elif pin == 5:	pin = "%"
		elif pin == 6:	pin = "&"
		elif pin == 7:	pin = "/"
		value = self.analogRead(pin)
		if not value:
			value = self.analogRead(pin)
		return value
	def analogReadLigth(self):
		pin = "("
		value = self.analogRead(pin)
		if not value:
			value = self.analogRead(pin)
		return value

	def readAll(self): return self.analogRead(")")
		
		
		
		
		
		

