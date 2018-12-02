import socket
import time
import picamera

from common import HOST, STREAM_PORT, DETECTOR_PORT

stream_socket = socket.socket()
stream_socket.connect((HOST, STREAM_PORT))
stream_connection = stream_socket.makefile('wb')
print("Stream connection established")

detector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
detector_socket.connect((HOST,PORT))
print("Detector connection established")

try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24
    camera = init_camera()
    camera.start_preview()
    time.sleep(2)
    camera.start_recording(stream_connection, format='h264')

    while True:
        print("Camera recording 1 sec")
        camera.wait_recording(1)

        print("Sending detector image")
        detector_socket.sendall(b'%f,%f' % (num1, num2))

        print("Receiving controller response")
        response = s.recv(1024)
        print("Received response:", response.decode())
finally:
    camera.stop_recording()
    stream_connection.close()
    stream_socket.close()
    detector_socket.close()
