import socket
import os

filename = "posts.json"
enc = "utf-8"
filesize = os.path.getsize(filename)

with socket.create_connection(("127.0.0.1", 30000)) as sock:
    s = input()
    s = s + ' ' + str(filesize)
    sock.sendall(s.encode(enc))
    with open(filename, 'r', encoding=enc) as f:
        data = f.read()
        sock.sendall(data.encode(enc))
    size = sock.recv(10)
    size = int(size.decode(enc))
    while size > 0:
        if size >= 1024:
            result = sock.recv(1024)
        else:
            result = sock.recv(size)
        size -= 1024
        print(result.decode(enc))
