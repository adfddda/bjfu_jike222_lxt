运行环境
Python 3.x
配置选项
服务器端和客户端运行在不同的操作系统上，确保它们可以相互访问。例如，可以将服务器端运行在Linux服务器上，而客户端运行在Windows或Linux等操作系统上。
确保客户端能够访问服务器的IP地址和端口。
程序运行步骤
打开终端或命令提示符。
启动服务器端程序，运行以下命令：
python server.py
服务器将开始监听来自客户端的连接请求，并模拟丢包和发送响应。
在另一个终端或命令提示符中，启动客户端程序，运行以下命令：
python client.py
客户端将向服务器发送12个请求，并模拟丢包和接收响应。
客户端将输出每个请求的发送和接收情况，以及通信性能的统计信息。
查看服务器和客户端的输出，以了解通信情况和性能统计。
注意事项
确保防火墙或网络设置不会阻止服务器和客户端之间的通信。
可以根据需要调整服务器端和客户端的配置选项，如IP地址、端口和丢包率等。
