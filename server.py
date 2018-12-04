import io
import struct
from PIL import Image
import numpy as np
import cv2
import socket
import subprocess
import _thread
import sys
import tty
import termios
from email_fsm import mail, send_email

from dog_detector import detect_dog
from common import HOST, STREAM_PORT, CONTROLLER_PORT, DETECTOR_PORT

# stream_socket = socket.socket()
# stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# stream_socket.bind((HOST, STREAM_PORT))
# stream_socket.listen(0)
# stream_connection = stream_socket.accept()[0].makefile('rb')
# print("Stream connection established")

# controller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# controller_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# controller_socket.bind((HOST, CONTROLLER_PORT))
# controller_socket.listen()
# controller_connection, _ = controller_socket.accept()
# print("Controller connection established")

detector_socket = socket.socket()
detector_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
detector_socket.bind((HOST, DETECTOR_PORT))
detector_socket.listen(0)
detector_connection = detector_socket.accept()[0].makefile('rb')
print("Detector connection established")

angle = 0

def controller_thread():
    global controller_socket, controller_connection, angle
    try:
        while True:
            print("Receiving ping from client")
            detector_data = controller_connection.recv(1024)
            print("Writing to detector")
            controller_connection.sendall(str(angle).encode())
    finally:
        controller_connection.close()
        controller_socket.close()

def detector_thread():
    global detector_connection
    try:
        while True:
            image_stream = None
            image_len = struct.unpack('<L', detector_connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                continue
            
            print("Received image")
            image_stream = io.BytesIO()
            image_stream.write(detector_connection.read(image_len))
            image_stream.seek(0)

            file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cv2.imwrite("out.jpg", img)

            image = Image.open("out.jpg")
            dog_detected = detect_dog(image)
            if mail(dog_detected):
                send_email()
            print("\t", "Dog?", dog_detected)

    finally:
        detector_connection.close()
        detector_socket.close()

# https://raspberrypi.stackexchange.com/questions/34336/how-to-capture-keyboard-in-python
def get_key_press():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def input_thread():
    global angle
    while True:
        char = get_key_press()
        if ord(char) == 3:  # ctrl-c
            break
        elif char == 'a':   # decrement
            angle -= 15
        elif char == 'd':   # increment
            angle += 15
        print("Angle is now:", angle)

if __name__ == "__main__":
    # _thread.start_new_thread(controller_thread, ())
    # _thread.start_new_thread(input_thread, ())
    _thread.start_new_thread(detector_thread, ())
    try:
        cmdline = ['vlc', '--demux', 'mjpeg', '-']
        # player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        while True:
            # stream_data = stream_connection.read(1024)
            # player.stdin.write(stream_data)
            continue
    finally:
        stream_connection.close()
        stream_socket.close()
        player.terminate()
        sys.exit()
