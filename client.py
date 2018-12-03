import socket
import time
import picamera
import _thread
from common import HOST, STREAM_PORT, DETECTOR_PORT

stream_socket = socket.socket()
stream_socket.connect((HOST, STREAM_PORT))
stream_connection = stream_socket.makefile('wb')
print("Stream connection established")

detector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
detector_socket.connect((HOST,DETECTOR_PORT))
print("Detector connection established")

def detector_thread():
    global detector_socket
    try:
        while True:
            time.sleep(1)
            print("Sending detector image")
            detector_socket.sendall(b'%f,%f' % (5, 2))

            print("Receiving controller response")
            angle = detector_socket.recv(1024).decode()
            print("Received response:", angle)
    finally:
        detector_socket.close()

if __name__ == "__main__":
    _thread.start_new_thread(detector_thread,())
    try:
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24
        camera.start_preview()
        time.sleep(2)
        camera.start_recording(stream_connection, format='h264')
        while True:
            pass
    finally:
        camera.stop_recording()
        stream_connection.close()
        stream_socket.close()
