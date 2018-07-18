import constants
import serial

print('imported serial')


class Bot:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)  # initialise the serial port
        self.init_angle = self.get_angle()  # Suyash
        print("Serial Port Initialized")

    def send(self, message):
        print("Sending :", message)
        self.ser.write(message.encode())
        self.wait_till_execution()

    def forward(self, time_in_ms):
        messg = "w" + str(time_in_ms)
        print("in forward")
        self.send(messg)

    def backward(self, time_in_ms):
        messg = "s" + str(time_in_ms)
        self.send(messg)

    def rotate(self, angle):  # angle is the relative angle
        # angle = angle - 90 + self.init_angle
        # angle = self.init_angle + angle - 90
        a = self.get_angle()
        angle = a - angle
        angle = angle % 360
        messg = "r" + str(angle)
        self.send(messg)
        self.send(messg)
        self.send(messg)
        self.send(messg)

    def get_angle(self):  # absoulte angle
        messg = "g"
        self.ser.write(messg.encode())
        _ = self.ser.readline()
        angle = self.ser.readline()[0:-2]
        return int(angle)

    def wait_till_execution(self):
        ack = self.ser.readline()
        ok = self.ser.readline()
        self.ser.close()
        self.ser.open()
        print("Executed....")
#bot = Bot()
#a = constants.avg_block_movement_time * 1 * 1000
#print(a)
#bot.forward(int(a))