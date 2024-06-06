import socket
import random
from datetime import datetime

# 定义常量
SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
DROP_RATE = 0.6  # 丢包率，假设为60%

# 创建UDP套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print("服务器已启动，等待连接...")

while True:
    message, client_address = server_socket.recvfrom(2048)
    seq_no = int.from_bytes(message[:2], 'big')
    ver = message[2]

    # 丢包模拟
    if random.random() < DROP_RATE:
        print(f"数据包 {seq_no} 被丢弃.")
        continue

    # 生成响应报文
    current_time = datetime.now().strftime('%H-%M-%S')
    response = seq_no.to_bytes(2, 'big') + bytes([ver]) + current_time.encode().ljust(200, b'\x00')

    server_socket.sendto(response, client_address)
    print(f"响应数据包 {seq_no} 已发送至 {client_address}")

# 关闭套接字
server_socket.close()
