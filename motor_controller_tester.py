import motor_controller

mc = MotorController()

setpoint = input('Enter the set-point in degrees: ')
while True:
    mc.control(setpoint)