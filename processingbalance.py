import time
from multiprocessing import Process
balance = 0#这是一个银行的存款
def change_it(n):
    global balance
    balance = balance + n#往银行存n元
    balance = balance - n#从银行提现n元
def run_thread(n):
    for i in range(100000):#运行十万次
        change_it(n)
    global balance
    print(balance)#运行十万次之后打印存款余额
t1 = Process(target=run_thread, args=(5,))#开启线程1，给入参5元
t2 = Process(target=run_thread, args=(8,))#开启线程2，给入参8元
t1.start()
t2.start()
t1.join()
t2.join()
