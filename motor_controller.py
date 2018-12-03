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
dtime2 = 5
speed = 15

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
        self.counter = 0
        self.self.start = 0
        self.start = clock()
        self.self.start2 = start
        self.clkLastState = GPIO.input(clk)
    
    def control(setpoint):
        global resolution,tolerance,dtime,dtime2,speed
        try:
            self.myMotor.setSpeed(speed)
            
            if setpoint > angle + float(tolerance/resolution):
                self.myMotor.run(Adafruit_MotorHAT.FORWARD)
            elif setpoint < angle - float(tolerance/resolution):
                self.myMotor.run(Adafruit_MotorHAT.BACKWARD)
            else:
                self.myMotor.run(Adafruit_MotorHAT.RELEASE)
            dtState = GPIO.input(dt)
            clkState = GPIO.input(clk)
            if clkState != self.clkLastState:
                if dtState != clkState:
                    self.counter += 1
                else:
                    self.counter -= 1
            self.clkLastState = clkState
            if clock() > self.start + dtime:
                self.angle = self.angle + float(counter)/(float(resolution))
                self.counter = 0
                self.start = clock()
            if clock() > self.start2 + dtime2:
                self.start2 = clock()
                print("Send Image")
        finally:
            pass

    # recommended for auto-disabling motors on shutdown!
    def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    