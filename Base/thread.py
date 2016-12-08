# coding=utf-8

import time
import Queue
import threading

# 并发线程总数
THREAD_COUNT = 2
# 任务数
JOB_COUNT = 10

# 任务队列
taskQueue = Queue.Queue()


# 具体的处理函数，负责处理单个任务
def do_something_using(arguments):
    print arguments


# 工作进程，负责不断地从队列中取数据并处理
def worker():
    while True:
        arguments = taskQueue.get()
        do_something_using(arguments)
        time.sleep(1)
        taskQueue.task_done()


# fork THREAD_COUNT个线程等待队列
for i in range(THREAD_COUNT):
    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()

# 把任务加入队列
for i in range(JOB_COUNT):
    taskQueue.put('job' + str(i))

# 等待所有任务完成
taskQueue.join()
