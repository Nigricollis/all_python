import requests

proxies = {
    'http': 'socks5://user:pass@host:port',
    'https': 'socks5://user:pass@host:port'
}

dest_path = r'D:\all_python\hikvision\sockaddress'
with open(dest_path,'r') as f:
	for ip in f.readlines():
		proxies['http']='socks5://'+ip.strip('\n')+':1080'
		proxies['https']='socks5://'+ip.strip('\n')+':1080'
		print ip.strip('\n')
		try:
			r = requests.get('http://www.sina.com.cn',proxies=proxies,timeout=3)
			if r.status_code == 200:
				print 'ok'
		except requests.exceptions.RequestException, e:
			continue


