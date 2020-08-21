import serial

class Bot:
	
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyUSB0',9600)	#initialise the serial port
		print("Serial Port Initialized")
	
	def send(self,message):
		print("Sending :",message)
		self.ser.write(message.encode())
		self.wait_till_execution()	

	def forward(self,time_in_ms):
		messg = "w"+str(time_in_ms)
		print("in forward")
		self.send(messg)
	def backward(self,time_in_ms):
		messg = "s"+str(time_in_ms)
		self.send(messg)
	def rotate(self,angle):
		if angle >=0 and angle <=360:
			messg = "e" +str(angle)
			self.send(messg)
		else:
			print("Invalid Angle Input")

	def wait_till_execution(self):
		ack = self.ser.readline()
		ok = self.ser.readline()


bot = Bot()
bot.forward(2000)
print("Instruction Complete")
