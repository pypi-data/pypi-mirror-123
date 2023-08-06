import paramiko


def ssh_exec_command(host, password, cmd, username='root', port=22):
    """[ssh远程linux主机执行命令]

    Args:
        host ([str]): [远程linux主机ip]
        password ([str]): [远程linux主机密码]
        cmd ([str]): [shell命令]
        port (str, optional): [远程linux主机端口号]. Defaults to '22'.
        username (str, optional): [远程linux主机用户名]. Defaults to 'root'.

    Returns:
        [str]: [result]
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        outputBytes = stdout.read() + stderr.read()
        outputStr = outputBytes.decode('utf8')
        ssh.close()
        return outputStr        # 返回命令结果

    except Exception as err:
        return err



def sftp_push_file(host, password, local_file, remote_file, username='root', port=22):
    """[sftp上传文件到目标主机]

    Args:
        host ([str]): [远程linux主机ip]
        password ([str]): [远程linux主机密码]
        local_file ([type]): [本地文件绝对路径]
        remote_file ([type]): [目标主机文件绝对路径]
        port (str, optional): [远程linux主机端口号]. Defaults to '22'.
        username (str, optional): [远程linux主机用户名]. Defaults to 'root'.

    Returns:
        [str]: ['0'上传成功]
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        ssh.close()
        return '0'

    except Exception as err:
        return err

