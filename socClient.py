import socket
import numpy as np
import pickle

def soc_recv():
    ip = '192.168.1.3'
    port = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        print("Connected to the server.")
        buffer = b''
        while True:
            packet = s.recv(4096)
            if not packet:
                break
            buffer += packet

            while b'END_OF_DATA' in buffer:
                data, buffer = buffer.split(b'END_OF_DATA', 1)
                array = pickle.loads(data)
                print("Received array:")
                print(array)

            

if __name__ == "__main__":
    soc_recv()
