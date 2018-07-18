import serial

ser = serial.Serial('/dev/ttyUSB0',9600)

while True:
	x = input("Enter A Command:")
	if x=="q":
		break;
	else:
		ser.write(x.encode())
		ack = ser.readline()
		print(ack)
		ok = ser.readline()
		print(ok)
		ser.close()
		ser.open()

ser.close()
