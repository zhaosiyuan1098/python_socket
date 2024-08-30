import socket
import numpy as np
import pickle
import threading

def generate_random_array():
    # Generate a random 4x4 array
    return np.random.rand(4, 4)

trans_to_send = generate_random_array()

class SocServer:
    """
    A class representing a server for socket communication.

    Attributes:
        ip (str): The IP address to bind the server to. Default is '127.0.0.1'.
        port (int): The port number to bind the server to. Default is 65434.
        socket (socket.socket): The socket object used for communication.
        conn (socket.socket): The connection object after successful connection.

    Methods:
        start(): Starts the server and listens for incoming connections.
        send(): Sends randomly generated array data to the client.
        receive(): Receives and deserializes array data from the client.
        close(): Closes the socket connection.
    """

    def __init__(self, ip='127.0.0.1', port=65434):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None

    def start(self):
        """
        Starts the server and listens for incoming connections.
        """
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        print("Server started. Listening for incoming connections...")
        self.conn, addr = self.socket.accept()
        print("Connected to client:", addr)

    def send(self):
        """
        Sends randomly generated array data to the client.
        """
        while True:
            c = generate_random_array()
            serialized_data = pickle.dumps(c)
            self.conn.sendall(serialized_data)
            self.conn.sendall(b'END_OF_DATA')
            print("Sent array:")
            print(c)

    def receive(self):
        """
        Receives and deserializes array data from the client.
        """
        buffer = b''
        while True:
            packet = self.conn.recv(4096)
            if not packet:
                break
            buffer += packet

            while b'END_OF_DATA' in buffer:
                data, buffer = buffer.split(b'END_OF_DATA', 1)
                array = pickle.loads(data)
                print("Received array:")
                print(array)

    def close(self):
        """
        Closes the socket connection.
        """
        self.conn.close()
        self.socket.close()

if __name__ == "__main__":
    soc_server = SocServer()
    soc_server.start()

    send_thread = threading.Thread(target=soc_server.send)
    receive_thread = threading.Thread(target=soc_server.receive)
    send_thread.start()
    receive_thread.start()
