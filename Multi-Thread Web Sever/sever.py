from socket import *
import threading # 引入线程模块
import os

# 针对线程使用编写的函数
def Server(ClientSock, addr):
    BUFSIZE = 1024 # 将缓冲区大小设置为 1KB
    print('connected from:', addr) 
    recData = ClientSock.recv(BUFSIZE)# 从socket中接受一个数据，最大长度为BUFSIZE
    data = recData.decode()# 将数据解码

    # 当服务器未收到返回信息，即data长度为0，直接退出
    if len(data) == 0:
        ClientSock.close()
        return 

    directory = os.getcwd() # 服务器端可访问的文件目录：当前工作的目录
    print("***************************************************\n")
    index = 4 # 检索文件的搜索路径
    
    # 找到路径
    while data[index] != ' ':
        index += 1
    
    # 如果检索文件为空，则默认导向访问成功的页面
    if index == 5 : direction = os.path.join(directory, "Success.html") 
    else: direction = os.path.join(directory, data[5 : index]) # 用os的方法拼接出完整的路径
    
    # 如果路径存在，本服务器默认只支持访问html文件
    if os.path.exists(direction) and direction.endswith(".html"):
        file=open(direction,encoding="utf-8") # 打开路径中的文件
        SUCCESS_PAGE = "HTTP/1.1 200 OK\r\n\r\n" + file.read() # 构造成功报文反馈给服务器
        print(SUCCESS_PAGE)
        ClientSock.sendall(SUCCESS_PAGE.encode()) # 正常访问，发送客户端需求的文件
        ClientSock.close() # 关闭针对目前客户建立的套接字
    
    # 如果路径不存在，返回失败页面
    else:
        FAIL_PAGE = "HTTP/1.1 404 NotFound\r\n\r\n" + open(os.path.join(directory, "Fail.html")).read()
        print(FAIL_PAGE)
        ClientSock.sendall(FAIL_PAGE.encode()) # 给客户端返回访问失败的页面
        ClientSock.close() # 关闭针对目前客户建立的套接字
    

if __name__ =='__main__': 
    HOST = "" # HOST变量为空，是对 bind()方法的标识，表示可以使用任何可用的地址，此程序在什么主机上运行，HOST为该主机的IP地址
    PORT = 4004  # 随机设置的端口号，并且该端口号没有被使用或被系统保留
    ADDR = (HOST, PORT) # 地址 = IP + 端口号
    SeverSocket = socket(AF_INET, SOCK_STREAM) # 创建一个套接字对象
    SeverSocket.bind(ADDR) # 将套接字绑定到服务器地址
    SeverSocket.listen(5) # 启用服务器的监听，调用参数是在连接被转接或拒绝之前，传入连接请求的最大数，此处说明允许传入链接请求数为5
    print("waiting for connection......\n")                  
    while True:  #进入无限循环
        ClientSock, addr = SeverSocket.accept() 
        # 调用 accept()函数之后，就开启了一个单线程服务器，它会等待客户端的连接，处于阻塞状态，直至一个连接到达
        thread = threading.Thread(target=Server, args=(ClientSock, addr))  
        thread.start() # 开始执行该线程