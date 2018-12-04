import time
import atexit
from RPi import GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

########################################################################################################################
# motor init
########################################################################################################################
mh = Adafruit_MotorHAT(addr=0x60)
def turnOffMotors():
    for i in [1, 2, 3, 4]: mh.getMotor(i).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)
motor = mh.getMotor(3)
motor.run(Adafruit_MotorHAT.FORWARD)
lastDirection = Adafruit_MotorHAT.FORWARD

########################################################################################################################
# encoder init
########################################################################################################################
SLEEP = 0.00001
CLK_PIN = 17
DT_PIN = 18
TICKS_PER_ROTATION = 1100 # empirically derived

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter, counterTime = 0, 0
MAX_COUNT = 100
lastClkState = GPIO.input(CLK_PIN)

########################################################################################################################
# controller init
########################################################################################################################
KP = 7          # proportional controller constant
THRESH = 150    # controller max output
TOLERANCE = 2   # error tolerance (degrees)

########################################################################################################################
# main
########################################################################################################################
class MotorController():
	def __init__(self):
		pass

	def control(setpoint):
		global motor, lastDirection, SLEEP, CLK_PIN, DT_PIN, TICKS_PER_ROTATION
		global counter, counterTime, MAX_COUNT, lastClkState
		global KP, THRESH, TOLERANCE

		clkState = GPIO.input(CLK_PIN)
		dtState = GPIO.input(DT_PIN)
		if clkState != lastClkState and dtState != clkState:
			counter -= 1
		elif clkState != lastClkState:
			counter += 1
		lastClkState = clkState
		counterTime = counterTime + 1

		if counterTime == MAX_COUNT:
			counterTime = 0
			
			motorAngle = (counter / TICKS_PER_ROTATION * 360) % 360
			error = setpoint - motorAngle
			if error > 180: # handle discontinuity about 360 and 0
				error = error - 360
			if error < -180:
				error = error + 360
			print("Angle:", motorAngle, "\t", "Error:", error)
			
			motorCommand = int(abs(error)) * KP
			if abs(error) < TOLERANCE:
				motorCommand = 0
			elif motorCommand > THRESH:
				motorCommand = THRESH
			motorDirection = Adafruit_MotorHAT.BACKWARD if error >= 0 else Adafruit_MotorHAT.FORWARD
			
			if motorDirection != lastDirection:
				motor.run(motorDirection)
			motor.setSpeed(motorCommand)
			lastDirection = motorDirection
		time.sleep(SLEEP)