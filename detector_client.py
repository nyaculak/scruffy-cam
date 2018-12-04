import socket
import time
import picamera
from common import HOST, DETECTOR_PORT

detector_socket = socket.socket()
detector_socket.connect((HOST, DETECTOR_PORT))
detector_connection = detector_socket.makefile('wb')
print("Detector connection established")

if __name__ == "__main__":
    try:
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24
        time.sleep(2)
        
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg'):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))
    finally:
        camera.stop_recording()
        detector_connection.close()
        detector_socket.close()
