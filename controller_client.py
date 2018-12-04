import socket
import time
import picamera
import _thread
from common import HOST, STREAM_PORT, CONTROLLER_PORT
from motor_controller import MotorController

setpoint = 0
motor_controller = MotorController()

stream_socket = socket.socket()
stream_socket.connect((HOST, STREAM_PORT))
stream_connection = stream_socket.makefile('wb')
print("Stream connection established")

controller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller_socket.connect((HOST,CONTROLLER_PORT))
print("Detector connection established")

def controller_thread():
    global controller_socket, setpoint
    try:
        while True:
            time.sleep(.1)
            print("Pinging server")
            controller_socket.sendall(b'ping')
            print("Receiving controller response")
            angle = controller_socket.recv(1024).decode()
            setpoint = int(angle)
    finally:
        controller_socket.close()

if __name__ == "__main__":
    _thread.start_new_thread(controller_thread,())
    try:
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24
        time.sleep(2)
        camera.start_recording(stream_connection, format='mjpeg')
        while True:
            motor_controller.control(setpoint)
    finally:
        camera.stop_recording()
        stream_connection.close()
        stream_socket.close()
