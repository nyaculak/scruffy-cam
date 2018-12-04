import socket
import subprocess
import _thread
import sys
import tty
import termios
from common import HOST, STREAM_PORT, DETECTOR_PORT

stream_socket = socket.socket()
stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
stream_socket.bind((HOST, STREAM_PORT))
stream_socket.listen(0)
stream_connection = stream_socket.accept()[0].makefile('rb')
print("Stream connection established")

detector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
detector_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
detector_socket.bind((HOST, DETECTOR_PORT))
detector_socket.listen()
detector_connection, _ = detector_socket.accept()
print("Detector connection established")

angle = 0

def detector_thread():
    global detector_socket, detector_connection, angle
    try:
        while True:
            print("Receiving ping from client")
            detector_data = detector_connection.recv(1024)
            print("Writing to detector")
            detector_connection.sendall(str(angle).encode())
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
    _thread.start_new_thread(detector_thread, ())
    _thread.start_new_thread(input_thread, ())
    try:
        cmdline = ['vlc', '--demux', 'mjpeg', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        while True:
            stream_data = stream_connection.read(1024)
            player.stdin.write(stream_data)
    finally:
        stream_connection.close()
        stream_socket.close()
        player.terminate()
        sys.exit()
