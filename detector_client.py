import socket
import time
import picamera
from common import HOST, DETECTOR_PORT

detector_socket = socket.socket()
detector_socket.connect((HOST, DETECTOR_PORT))
detector_connection = detector_socket.makefile('wb')
print("Detector connection established")

if __name__ == "__main__":
    pass
