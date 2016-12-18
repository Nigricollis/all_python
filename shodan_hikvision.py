#coding:utf-8
import shodan
SHODAN_API_KEY='rHRbstt6uayzsIaTe22AQmyLx12bGfx2'

api = shodan.Shodan(SHODAN_API_KEY)

try:
	results = api.search('hikvision RTSP')
	
	with open(r'D:\all_python\hikvision\result.txt','w') as f:
		for result in results['matches']:
			f.write(result['ip_str']+'\n')
	
except shodan.APIError, e:
	print 'ERROR: %s' % e