import socket
import numpy as np
import pickle
import threading

def generate_random_array():
    # 生成一个随机的4x4的数组
    return np.random.rand(4, 4)

trans_to_send = generate_random_array()

class SocClient:
    """
    A class representing a client for socket communication.

    Attributes:
        ip (str): The IP address of the server to connect to. Default is '127.0.0.1'.
        port (int): The port number of the server to connect to. Default is 65434.
        socket (socket.socket): The socket object used for communication.
        conn (socket.socket): The connection object after successful connection.

    Methods:
        connect(): Connects to the server.
        send(): Sends randomly generated array data to the server.
        receive(): Receives and deserializes array data from the server.
        close(): Closes the socket connection.
    """

    def __init__(self, ip='127.0.0.1', port=65434):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None

    def connect(self):
        """
        Connects to the server using the specified IP address and port number.
        """
        self.socket.connect((self.ip, self.port))
        print("已连接到服务器。")

    def send(self):
        """
        Sends randomly generated array data to the server.
        """
        while True:
            c = generate_random_array()
            serialized_data = pickle.dumps(c)
            self.socket.sendall(serialized_data)
            self.socket.sendall(b'END_OF_DATA')
            print("发送的数组：")
            print(c)

    def receive(self):
        """
        Receives and deserializes array data from the server.
        """
        buffer = b''
        while True:
            packet = self.socket.recv(4096)
            if not packet:
                break
            buffer += packet

            while b'END_OF_DATA' in buffer:
                data, buffer = buffer.split(b'END_OF_DATA', 1)
                array = pickle.loads(data)
                print("接收到的数组：")
                print(array)

    def close(self):
        """
        Closes the socket connection.
        """
        self.socket.close()

if __name__ == "__main__":
    soc_client = SocClient()
    soc_client.connect()

    send_thread = threading.Thread(target=soc_client.send)
    receive_thread = threading.Thread(target=soc_client.receive)
    send_thread.start()
    receive_thread.start()
