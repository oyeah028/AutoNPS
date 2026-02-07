import paramiko
import re
import json
import os
import sys

host = ""
username = ""
passwd = ""

# 读取配置
with open("config.json", "r") as f:
    data = json.load(f)
    host = data['host']
    username = data['username']
    passwd = data['password']

    # 验证地址格式
if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host):
    print("输入的IP地址格式不正确;")


# 实例化SSHClient 
ssh_client = paramiko.SSHClient()   
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   

try:
    # 连接服务器
    ssh_client.connect(hostname=host, port=22, username=username, password=passwd) 
except:
    print("连接失败，请检查用户名和密码是否正确;")
    sys.exit(0)

commandList = [
    "mkdir -p /home/NpsServer",  # 使用绝对路径确保目录创建在正确位置
]

for command in commandList:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    # 检查命令执行结果
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        print(f"命令执行失败: {command}")
        print(f"错误信息: {stderr.read().decode('utf-8')}")
        sys.exit(0)
    else:
        print(f"命令执行成功: {command}")

# 验证远程目录是否存在
check_dir = "ls -la /home/"
stdin, stdout, stderr = ssh_client.exec_command(check_dir)
exit_status = stdout.channel.recv_exit_status()
if exit_status == 0:
    print("远程服务器/home目录内容:")
    print(stdout.read().decode('utf-8'))
else:
    print(f"检查目录失败: {stderr.read().decode('utf-8')}")
    sys.exit(0)

# 文件传输功能
try:
    # 检查当前工作目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 检查本地文件是否存在
    local_file = "nps.tar.gz"  # 需要上传的本地文件
    if os.path.exists(local_file):
        print(f"本地文件 {local_file} 存在")
        print(f"文件大小: {os.path.getsize(local_file)} 字节")
    else:
        print(f"本地文件 {local_file} 不存在")
        # 尝试使用绝对路径
        local_file = os.path.join(current_dir, "nps.tar.gz")
        print(f"尝试使用绝对路径: {local_file}")
        if not os.path.exists(local_file):
            print("文件仍然不存在，请检查文件是否存在于当前目录")
            sys.exit(0)
    
    # 创建SFTP客户端
    sftp_client = ssh_client.open_sftp()
    
    # 远程文件路径
    remote_file = "/home/NpsServer/nps.tar.gz"  # 目标服务器上的文件路径
    
    print(f"正在上传文件 {local_file} 到 {remote_file}...")
    # 上传文件
    sftp_client.put(local_file, remote_file)
    print("文件上传成功!")
    
    # 关闭SFTP客户端
    sftp_client.close()
except Exception as e:
    print(f"文件传输失败: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(0)

# 验证上传的文件是否存在于远程服务器
verify_file = "ls -la /home/NpsServer/"
stdin, stdout, stderr = ssh_client.exec_command(verify_file)
print(stdout.read().decode('utf-8'))
exit_status = stdout.channel.recv_exit_status()

# 使用绝对路径执行解压缩命令
commandList = [
    "cd /home/NpsServer && tar -xzvf nps.tar.gz",  # 确保在正确目录下执行
    "ls -la /home/NpsServer/",  # 检查解压缩后的内容
    "nohup /home/NpsServer/NpsServer/nps > /home/NpsServer/nps.log 2>&1 &",  # 启动NPS服务器
]

for command in commandList:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print(stdout.read().decode('utf-8'))
    

conf = f"""
[common]
server_addr={host}:8024
conn_type=tcp
vkey=8wfgi3dwv6hwf8zg
auto_reconnection=true
max_conn=1000
flow_limit=1000
rate_limit=1000
basic_username=11
basic_password=3
web_username=user
web_password=1234
crypt=true
compress=true
#pprof_addr=0.0.0.0:9999
disconnect_timeout=60

[health_check_test1]
health_check_timeout=1
health_check_max_failed=3
health_check_interval=1
health_http_url=/
health_check_type=http
health_check_target=127.0.0.1:8083,127.0.0.1:8082

[health_check_test2]
health_check_timeout=1
health_check_max_failed=3
health_check_interval=1
health_check_type=tcp
health_check_target=127.0.0.1:8083,127.0.0.1:8082

"""

port_list = data['port']


for port in port_list:
    conf += f"""
[tcp_{port}]
mode=tcp
target_addr=127.0.0.1:{port}
server_port={port}
"""

with open("npc/conf/npc.conf", "w") as f:
    f.write(conf)

os.system(os.getcwd() + "\\npc\\npc.exe")
