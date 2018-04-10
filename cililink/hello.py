import redis

ip = '127.0.0.1'
password = ''
pool = redis.ConnectionPool(host=ip, port=6379, db=0, password=password)
r = redis.Redis(connection_pool=pool)
r.set('hello','world')