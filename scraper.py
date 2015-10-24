from datetime import date, timedelta
from time import strftime, sleep
from random import randint
from sys import argv
import json
import urllib
import urllib.request

import settings

if len(argv) < 2 or not settings.STATIONS.get(argv[1], False):	
	stations = ', '.join( settings.STATIONS.keys() )	
	print('You must specify the station: %s' % stations)	
	exit()


station_name = argv[1]
for i in range(1,357):
	yesterday = date.today() - timedelta(i)	
	url = "http://powietrze.katowice.wios.gov.pl/dane-pomiarowe/pobierz"
	
	params = {
		"measType":"Auto",
		"viewType":"Station",
		"dateRange":"Day",
		"date": yesterday.strftime("%d.%m.%Y")
	}
	
	station = settings.STATIONS[station_name]	
	params.update( station['query'] )	
	data = urllib.parse.urlencode({ 'query': json.dumps(params) })
	data = data.encode('utf-8')

	sleep(randint(1,3))
	req = urllib.request.Request(url, data)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	
	response_json = json.loads(respData.decode("utf-8"))
	
	for series in response_json["data"]["series"]:
		series_id = series["paramId"]
		for data in series["data"]:
			
			print(','.join([ str(station_name), str(series_id), str(data[0]), str(data[1]) ]))