'''
Extended FSM to control the motor
'''

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import clock
import atexit
from RPi import GPIO

#Motor encoder pins
clk = 17
dt = 18

#Motor controller constants
resolution = 1333
tolerance = 5
dtime = 0.1

class MotorController():
	def __init__(self):
		global clk, dt
		mh = Adafruit_MotorHAT(addr=0x60)
		atexit.register(turnOffMotors)
		self.myMotor = mh.getMotor(3)
		self.myMotor.run(Adafruit_MotorHAT.RELEASE)
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		
		self.angle = 0
		self.speed = 15
    
	def control(setpoint):
		global resolution,tolerance,dtime
		counter = 0;
		clkLastState = GPIO.input(clk)
		delta = setpoint - self.angle
		try:
			self.myMotor.setSpeed(self.speed)
			start = clock()
			while True:
				if delta > float(tolerance/resolution):
					self.myMotor.run(Adafruit_MotorHAT.FORWARD)
				elif delta < -float(tolerance/resolution):
					self.myMotor.run(Adafruit_MotorHAT.BACKWARD)
				else:
					break;
				dtState = GPIO.input(dt)
				clkState = GPIO.input(clk)
				if clkState != clkLastState:
					if dtState != clkState:
						counter += 1
					else:
						counter -= 1
				clkLastState = clkState
				if clock() > start + dtime:
					delta -= float(counter)/(float(resolution))
					counter = 0
					start = clock()
		finally:
			GPIO.cleanup()
			self.myMotor.run(Adafruit_MotorHAT.RELEASE)
			self.angle = setpoint

	# recommended for auto-disabling motors on shutdown!
	def turnOffMotors():
		mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
		mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
		mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
		mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    