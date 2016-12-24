#import nmap
import requests
import threading
import requests
import base64
import ipaddress
#############################################################################################################################
#def nmap_hosts():
#	dest_list = []
#	nm = nmap.PortScanner()
#	nm.scan('10.72.15.0/24','554')
#	for host in nm.all_hosts():
#		#if nm[host]['tcp'][554]['state'] == 'open':
#		dest_list.append(host)
#	print dest_list
#	return dest_list
#############################################################################################################################


def all_scan(dest_list):
	username = 'admin'
	password='12345'
	userNamePass=base64.b64encode(username+':'+password)
	headers ={
		'Host':'',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
		'Accept':'*/*',
		'Accept-Language':'en;q=0.3',
		'Accept-Encoding':'gzip, deflate',
		'If-Modified-Since':'0',
		'Authorization':'Basic '+userNamePass,
		'X-Requested-with':'XMLHttpRequest',
		'Referer':'',
		'Connection':'keep-alive'
		}
	cookies =dict(language='en',updateTips='true')
	threads = []
	screenLock = threading.Semaphore(value=1)
	def scan(dest_address,headers,cookies):
		try:
			r = requests.get(dest_address,headers=headers,cookies=cookies,timeout=10)
#			if r.status_code == 200:
			if r.status_code == 200 and r.text.startswith('<?xml'):
				screenLock.acquire()
				print dest_address
		except requests.exceptions.RequestException, e:
			screenLock.acquire()
			#print dest_address
			#raise e
		finally:
			screenLock.release()


	for ip in dest_list:
		ip = str(ip)
		headers['Host']=ip
		headers['Referer']="http://" + ip+"/doc/page/login.asp"
		dest_address = "http://"+ ip +"/PSIA/Custom/SelfExt/userCheck"
		#dest_address = "http://" + ip +"/ISAPI/Security/userCheck"
		#print headers
		threads.append(threading.Thread(target=scan,args=(dest_address,headers,cookies)))
		#scan(dest_address,headers,cookies)
	for t in threads:
	 	t.setDaemon(False)
	 	t.start()


def main():
	dest_list = ipaddress.ip_network(u'10.72.0.0/16')
	all_scan(dest_list)

if __name__ == '__main__':
	main()