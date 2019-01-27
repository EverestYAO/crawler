
# 监听本机的5000端口
bind = '0.0.0.0:5000'
preload_app = True

# 支持最大并发查询数
workers=8
#workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "egg:meinheld#gunicorn_worker"
# 每个进程的开启线程
threads = 8
#允许等待最大人数
backlog = 2048

# 工作模式为gevent
reload = True
debug=True
# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
# 进程名称
proc_name = 'leon.pid'
# 进程pid记录文件
pidfile = 'app_pid.log'
loglevel = 'debug'
logfile = 'debug.log'
accesslog = 'access.log'
timeout = 60
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
