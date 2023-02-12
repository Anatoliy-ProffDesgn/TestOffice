import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.sendto(b'q', ('127.0.0.1',8888))