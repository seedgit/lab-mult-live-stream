# This code is for the server
# Lets import the libraries
from sqlite3 import connect
import sys
import socket, cv2, pickle, struct, imutils
port = 9999
if len(sys.argv) > 1:
    port = int(sys.argv[1])

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('HOST IP:', host_ip)

socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)
connected = False
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    connected = True
    if client_socket:
        while True:
            vid = cv2.VideoCapture('../video/sample.mp4')
            while (vid.isOpened()):
                img, frame = vid.read()
                if not img:
                    break
                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame) #serialize frame to bytes
                message = struct.pack("Q", len(a)) + a # pack the serialized data
                # print(message)
                try:
                    client_socket.sendall(message) #send message or data frames to client
                except Exception as e:
                    connected = False
                    break
            if not connected:
                break
socket.close()