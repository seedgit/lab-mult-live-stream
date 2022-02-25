import sys
import socket, pickle, struct
import cv2
from threading import Thread
import time
import multiprocessing

# create socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

def display_stream(port):
    connected = False
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while not connected:
        try:
            node_socket.connect((host_ip, port))
            connected = True
        except Exception as e:
            pass

    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = node_socket.recv(4 * 1024)
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += node_socket.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow(f"RECEIVING VIDEO {port}", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # press q to exit video
            break

port = 9999
if len(sys.argv) > 1:
    port = int(sys.argv[1])

print(f'start listen at port {port}')
display_stream(port)