import socket

host = "prog27"
ip = socket.gethostbyname(host)
print(ip)
porta = 22222

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((ip, porta)) 

b = conn.recv(2048)
s = b.decode('utf-8')
print(s)
input()