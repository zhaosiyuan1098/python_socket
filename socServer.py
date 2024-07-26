import socket
import numpy as np
import pickle
import threading

def generate_arrays():
    # 生成随机的彩色图像和深度图像
    color_image = np.random.randint(0, 256, size=(1280, 720, 3), dtype=np.uint8)
    depth_image = np.random.randint(0, 256, size=(1280, 720, 1), dtype=np.uint8)
    data = (color_image, depth_image)
    return data


class SocServer:
    """
    A class representing a socket server.

    Attributes:
        ip (str): The IP address to bind the server to. Default is '127.0.0.1'.
        port (int): The port number to bind the server to. Default is 65434.
        socket (socket.socket): The socket object used for communication.
        conn (socket.socket): The socket object representing the client connection.
        addr (tuple): The address of the client.

    Methods:
        start(): Binds the IP address and port number, and starts listening for connections.
        send(): Sends data to the connected client.
        receive(): Receives data from the connected client.
        close(): Closes the connection and the socket.

    Example:
        soc_server = SocServer()
        soc_server.start()
    """

    def __init__(self, ip='127.0.0.1', port=65434):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None

    def start(self):
        # 绑定IP地址和端口号，并开始监听连接
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        print(f"服务器正在监听 {self.ip}:{self.port}")
        self.conn, self.addr = self.socket.accept()
        print(f"已连接客户端 {self.addr}")

    def send(self):
        while True:
            if self.conn:
                # 生成数据并序列化
                c = generate_arrays()
                serialized_data = pickle.dumps(c)
                # 发送数据
                self.conn.sendall(serialized_data)
                # 发送终止符分割消息
                self.conn.sendall(b'END_OF_DATA')
                print(c)
            else:
                # 连接已关闭
                print("连接已关闭。")
                break

    def receive(self):
        while True:
            try:
                # 接收数据
                received_data = self.conn.recv(4096)
                if received_data:
                    # 处理接收到的数据
                    try:
                        received_array = pickle.loads(received_data)
                        if isinstance(received_array, np.ndarray) and received_array.shape == (4, 4):
                            print("接收到的数组:", received_array)
                        else:
                            print("接收到的数据格式不符合预期。忽略该消息。")
                    except Exception as e:
                        print("处理接收到的数据时发生错误:", str(e))
                else:
                    # 客户端关闭连接
                    print("客户端关闭连接。")
                    break
            except Exception as e:
                print("接收数据时发生错误:", str(e))
                break

    def close(self):
        if self.conn:
            self.conn.close()
        self.socket.close()

if __name__ == "__main__":
    soc_server = SocServer()
    soc_server.start()

    send_thread = threading.Thread(target=soc_server.send)
    receive_thread = threading.Thread(target=soc_server.receive)

    send_thread.start()
    receive_thread.start()
