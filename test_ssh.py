import paramiko

dest_path=r'D:\all_python\hikvision\sshaddress'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def my_ssh(dest):
	try:
		ssh.connect(dest,22,'root','111111',timeout=5)
		ssh.close()
		print dest + ' Success!'
	except Exception,e:
		print dest +' Failed!'

def main():
	with open(dest_path,'r') as f:
		for ip in f.readlines():
			my_ssh(ip.strip('\n'))

if __name__=='__main__':
	main()
