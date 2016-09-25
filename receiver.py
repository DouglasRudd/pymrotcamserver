import socket
import struct
receiver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receiver.bind(("127.0.0.1",5001))
while 1:
    buf, address = receiver.recvfrom(1024)
    value = struct.unpack("f",buf)
    print value
