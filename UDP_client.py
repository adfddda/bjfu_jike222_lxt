import socket
import time
import random
from datetime import datetime

# 定义常量
SERVER_IP = '127.0.0.1'  # 服务器IP地址
SERVER_PORT = 12345      # 服务器端口
NUM_PACKETS = 12         # 发送的请求报文数
TIMEOUT = 0.1            # 超时时间，单位为秒（100ms）

# 创建UDP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

# 跟踪统计信息
received_packets = 0
rtt_list = []
server_start_time = None
server_end_time = None

# 发送12个请求报文
for seq_no in range(1, NUM_PACKETS + 1):
    ver = 2  # 版本号
    message = seq_no.to_bytes(2, 'big') + bytes([ver]) + b'a' * 200  # 生成请求报文
    attempts = 0

    while attempts < 3:  # 最多重传两次
        attempts += 1
        try:
            start_time = time.time()
            client_socket.sendto(message, (SERVER_IP, SERVER_PORT))
            print(f"发送数据包 {seq_no}")

            response, server_address = client_socket.recvfrom(2048)
            rtt = (time.time() - start_time) * 1000  # 计算RTT，单位为毫秒
            received_seq_no = int.from_bytes(response[:2], 'big')
            received_ver = response[2]
            server_time = response[3:].decode().strip('\x00')

            if received_seq_no == seq_no and received_ver == ver:
                print(f"从 {server_address} 收到数据包 {seq_no} 的响应，RTT为 {rtt:.2f} 毫秒，服务器时间为 {server_time}")
                received_packets += 1
                rtt_list.append(rtt)
                if server_start_time is None:
                    server_start_time = datetime.strptime(server_time, '%H-%M-%S')
                server_end_time = datetime.strptime(server_time, '%H-%M-%S')
                break
            else:
                print(f"收到的响应数据包 {received_seq_no} 不正确，期待的是数据包 {seq_no}")
        except socket.timeout:
            print(f"请求 {seq_no} 在第 {attempts} 次尝试时超时")
            if attempts == 3:
                print(f"数据包 {seq_no} 在尝试 3 次后未能收到响应")

# 计算统计信息
if rtt_list:
    max_rtt = max(rtt_list)
    min_rtt = min(rtt_list)
    avg_rtt = sum(rtt_list) / len(rtt_list)
    stddev_rtt = (sum((rtt - avg_rtt) ** 2 for rtt in rtt_list) / len(rtt_list)) ** 0.5
    server_response_time = (server_end_time - server_start_time).total_seconds() if server_start_time and server_end_time else 0

    print(f"接收到的UDP数据包数量: {received_packets}")
    print(f"丢包率: {(1 - received_packets / NUM_PACKETS) * 100:.2f}%")
    print(f"最大RTT: {max_rtt:.2f} 毫秒")
    print(f"最小RTT: {min_rtt:.2f} 毫秒")
    print(f"平均RTT: {avg_rtt:.2f} 毫秒")
    print(f"RTT标准差: {stddev_rtt:.2f} 毫秒")
    print(f"服务器总响应时间: {server_response_time:.2f} 秒")

# 关闭套接字
client_socket.close()
