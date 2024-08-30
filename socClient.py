import socket
import numpy as np
import pickle
import threading

def generate_arrays():
    # Generate random color and depth images
    color_image = np.random.randint(0, 256, size=(1280, 720, 3), dtype=np.uint8)
    depth_image = np.random.randint(0, 256, size=(1280, 720, 1), dtype=np.uint8)
    data = (color_image, depth_image)
    return data


class SocClient:
    """
    A class representing a socket client.

    Attributes:
        ip (str): The IP address to connect to. Default is '127.0.0.1'.
        port (int): The port number to connect to. Default is 65434.
        socket (socket.socket): The socket object used for communication.

    Methods:
        connect(): Connects to the server.
        send(): Sends data to the server.
        receive(): Receives data from the server.
        close(): Closes the connection and the socket.

    Example:
        soc_client = SocClient()
        soc_client.connect()
    """

    def __init__(self, ip='127.0.0.1', port=65434):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        # Connect to the server
        self.socket.connect((self.ip, self.port))
        print(f"Connected to server {self.ip}:{self.port}")

    def send(self):
        while True:
            # Generate data and serialize it
            c = generate_arrays()
            serialized_data = pickle.dumps(c)
            # Send data
            self.socket.sendall(serialized_data)
            # Send termination delimiter
            self.socket.sendall(b'END_OF_DATA')
            print(c)

    def receive(self):
        while True:
            try:
                # Receive data
                received_data = self.socket.recv(4096)
                if received_data:
                    # Process received data
                    try:
                        received_array = pickle.loads(received_data)
                        if isinstance(received_array, np.ndarray) and received_array.shape == (4, 4):
                            print("Received array:", received_array)
                        else:
                            print("Received data format does not match the expected format. Ignoring the message.")
                    except Exception as e:
                        print("Error occurred while processing received data:", str(e))
                else:
                    # Server closed the connection
                    print("Server closed the connection.")
                    break
            except Exception as e:
                print("Error occurred while receiving data:", str(e))
                break

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    soc_client = SocClient()
    soc_client.connect()

    send_thread = threading.Thread(target=soc_client.send)
    receive_thread = threading.Thread(target=soc_client.receive)

    send_thread.start()
    receive_thread.start()