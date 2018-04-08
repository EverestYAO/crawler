import requests
import multiprocessing
from pymongo import MongoClient
import time
import redis

redispool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)  
r = redis.StrictRedis(connection_pool=redispool)  
while True:  
	task = r.brpop('tq', 0)  
	print (task[1].decode());  
	if task[1].decode() == 'action':
		url='http://www.baidu.com'
		db=MongoClient('127.0.0.1', 27017).test
		url='http://www.baidu.com'
		start = time.time()
		ippool = []
		for i in db.ippool.find({'verify':False}):
			ippool.append(i['ip'])
		def verify(ip):
				proxies = {
			  	'http': 'http://%s'%(ip),
				}

				try:
					res = requests.get(url, proxies=proxies,timeout=2)
					print(res.status_code)
					if res.status_code ==200 :
						db.ippool.insert({'ip':ip,'verify':True})
						print('insert finished'.center(50,"*"))
				except Exception as e:
					print(e)
		pool = multiprocessing.Pool(processes=10)
		pool.map(verify,ippool[:100])
		print(time.time()-start)
		print('finished')
			