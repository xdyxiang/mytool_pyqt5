import paramiko
import time

def init_ssh():
    # 实例化SSHClient
    client = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证
    client.connect(hostname='172.25.113.23', port=22, username='root', password='123456')
    # 打开一个Channel并执行命令
    stdin, stdout, stderr = client.invoke_shell('df -h ;cd;./a.sh;echo 00000')  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
    # 打印执行结果
    print(stdout.read().decode('utf-8'))

    # 关闭SSHClient
    client.close()

def init_ssh1():
    # 实例化SSHClient
    trans = paramiko.Transport(('172.25.113.23',22))
    # 自动添加策略，保存服务器的主机名和密钥信息
    trans.connect(username="root", password='123456')
    # 连接SSH服务端，以用户名和密码进行认证
    chan = trans.open_session()
    chan.settimeout(30)
    chan.get_pty()
    chan.invoke_shell()
    time.sleep(1)
    chan.send('./a.sh && echo "执行完成";exit || echo "执行失败";exit\n')
    while True:
        if chan.exit_status_ready():
            print(chan.exit_status_ready())
            break
        time.sleep(1)
        results = chan.recv(99999)
        print(results.decode('utf8'))

    chan1 = trans.open_session()
    chan1.get_pty()
    chan1.invoke_shell()
    time.sleep(1)
    chan1.send('./a.sh && echo "执行完成";exit || echo "执行失败";exit\n')
    while True:
        print(chan1.exit_status_ready())
        if chan1.exit_status_ready():
            print(chan1.exit_status_ready())
            break
        time.sleep(1)
        results = chan1.recv(99999)
        print(results.decode('utf8'))

    print(chan.exit_status_ready())
    print(chan1.exit_status_ready())
    trans.close()
    # while not channel.recv_ready():
    #     time.sleep(3)
    #
    # out = channel.recv(9999)
    # print(out.decode("ascii"))
    #
    # channel.send('cd ..\n')
    # channel.send('cd or_fail\n')
    # channel.send('ls\n')
    #
    # while not channel.recv_ready():
    #     time.sleep(3)

init_ssh1()
