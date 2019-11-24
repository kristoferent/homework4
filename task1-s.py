import socket
import threading
import multiprocessing
import os
import time
from pycorenlp import StanfordCoreNLP

enc = "utf-8"
batch_size = 1024

def process_request(conn, addr):
    print("connected client:", addr)
    with conn:
        data = conn.recv(15)
        k = data.decode(enc)
        command, size = k.split(' ')
        size = int(size)
        out = ""
        k = ""
        while size > 0:
            if size >= batch_size:
                data = conn.recv(batch_size)
            else:
                data = conn.recv(size)
            size -= batch_size
            k += data.decode(enc)
        if command == "STAT":
            pass
        elif command == "ENTI":
            data = ""
            k = k.split('", "')
            for i in range(len(k)):
                print(k[i])
                print('------------------------------------------------------')
                res = nlp.annotate(k[i], properties={
                                            'annotators': 'ner',
                                            'outputFormat': 'json',
                                            'timeout': 100000,
                                            })
                for sentence in res['sentences']:
                    for word in sentence['tokens']:
                        if word['ner'] != 'O':
                            out += word['word'] + ', '
        else:
            out = "Unknown command. Please try STAT or ENTI instead."
        conn.sendall(str(len(out.encode(enc))).encode(enc))
        time.sleep(1)
        conn.sendall(out.encode(enc))

def worker(sock):
    while True:
        conn, addr = sock.accept()
        print("pid", os.getpid())
        th = threading.Thread(target=process_request, args=(conn, addr))
        th.start()

nlp = StanfordCoreNLP('http://localhost:9000')

with socket.socket() as sock:
    sock.bind(("", 30000))
    sock.listen()
    
    workers_count = 3
    workers_list = [multiprocessing.Process(target=worker, args=(sock,))
                    for _ in range(workers_count)]
    
    for w in workers_list:
        w.start()
    
    for w in workers_list:
        w.join()
