import time, threading
import queue
 
balance = 0
workQueue = queue.Queue(10)#定义队列
workQueue.put(balance)#往队列中写入第一个初始余额0元
def change_it(n):
    global balance
    balance = workQueue.get()#从队列中提取余额
    balance = balance + n#往银行存n元
    balance = balance - n#从银行提现n元
    workQueue.put(balance)#将余额写入队列
def run_thread(n):
    for i in range(100000):#运行十万次
        change_it(n)
    global balance
    print(balance)#运行十万次之后打印存款余额
t1 = threading.Thread(target=run_thread, args=(5,))#开启线程1，给入参5元
t2 = threading.Thread(target=run_thread, args=(8,))#开启线程2，给入参8元
t1.start()
t2.start()
t1.join()
t2.join()
