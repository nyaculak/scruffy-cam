from motor_controller import MotorController

mc = MotorController()

setpoint = input('Enter the set-point in degrees: ')
setpoint = int(setpoint)
while True:
    mc.control(setpoint)