#引入threadpool
#import threadpool
import time
from concurrent.futures import ThreadPoolExecutor

#hello函数，根据入参执行睡眠
def hello(delay):
    print(f'此线程等待{delay}秒')
    time.sleep(delay)

if __name__ == '__main__':
    start = time.time()
    pool = ThreadPoolExecutor(5)
    delay_list=[1,2,3,4,5]
    pool.map(hello,delay_list)
    pool.shutdown(wait=True)
    print(time.time()-start)

##获取开始时间
#    start = time.time()
##创建线程池，指定5个线程
#    pool = threadpool.ThreadPool(5)
##创建任务列表    
#    delay_list=[1,2,3,4,5,6]
##创建任务
#    task = threadpool.makeRequests(hello,delay_list)
#    for i in task:
##通过遍历将任务传入线程池中执行
#        pool.putRequest(i)
##等待线程执行结束
#    pool.wait()
##打印代码运行花费的时间
#    print(time.time()-start)
#
