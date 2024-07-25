import socket
import numpy as np
import pickle

class SocServer:
    def __init__(self, ip='192.168.1.198', port=65432):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None

    def start(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        print(f"Server listening on {self.ip}:{self.port}")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected by {self.addr}")

    def send(self, data):
        if self.conn:
            serialized_data = pickle.dumps(data)
            self.conn.sendall(serialized_data)
            # 发送终止符分割消息
            self.conn.sendall(b'END_OF_DATA')
            print("Data sent.")

    def close(self):
        if self.conn:
            self.conn.close()
        self.socket.close()

def send():
    array1 = np.array([1, 2, 3, 4, 5])
    array2 = np.array([6, 7, 8, 9, 10])
    array3 = np.array([11, 12, 13, 14, 15])
    array = np.array([array1, array2, array3])
    for i in range(10):
        soc_server.send(array)
        print(f"Sent array {i}")

if __name__ == "__main__":
    soc_server = SocServer()
    soc_server.start()
    send()
