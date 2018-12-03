import socket
import subprocess
import _thread
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

def stream_thread():
    global stream_socket, stream_connection
    try:
        cmdline = ['vlc', '--demux', 'h264', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

        while True:
            stream_data = stream_connection.read(1024)
            player.stdin.write(stream_data)
    finally:
        stream_connection.close()
        stream_socket.close()
        player.terminate()

def detector_thread():
    global detector_socket, detector_connection
    try:
        while True:
            print("Reading detector data")
            detector_data = detector_connection.recv(1024)

            print("Writing to detector")
            angle = "60"
            detector_connection.sendall(str(angle).encode())
    finally:
        detector_connection.close()
        detector_socket.close()

if __name__ == "__main__":
    _thread.start_new_thread(stream_thread, ())
    _thread.start_new_thread(detector_thread, ())
    while True:
        pass
