#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Time: 2022/3/16 2:55 下午
@Author: y
@QQ: 77386059
@Wechat: Reny-ovo-
@Description: 将接口的入参以csv参数化文件的形式传入，并将数据进行循环
"""


import os, sys
dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir)


import json, queue, csv
from locust import SequentialTaskSet, HttpUser, between, task, tag, LoadTestShape, constant
from common import config

class TaskSuit(SequentialTaskSet):
    def on_start(self):
        self.headers = {"Content-Type": "application/json"}
        # self.username = "19999999999"
        # self.pwd = "qwe1234"
    
    @task  # 装饰器，说明下面是一个任务
    @tag("leave_1", "logincase")  # 标签可重复
    def login_case(self):
        try:
            url = '/authentication'  # 接口请求地址
            # data = {"username": self.get_username(), "password": self.get_password(), "userType": 1}
            data = self.parent.queueData.get()   # 获取队列里的数据
            self.parent.queueData.put_nowait(data)    # 再将取出的数据插入队尾，对数据进行循环使用
            a = self.client.post(url, data=json.dumps(data), headers=self.headers, catch_response=True,
                                name="case_2_login").json()
            print(data)
            print(a)
        except queue.Empty:
            print("no date")

    def on_stop(self):
        pass



class TaskPlan(HttpUser):
    tasks = [TaskSuit]
    wait_time = between(0.01, 3)
    
    queueData = queue.Queue()  # 队列实例化
    date = csv.reader(open(config.conf_path('date','test.csv'),'r'))
    for i in date:   # 循环数据生成
        queueData.put_nowait({
            "username": i[0],
            "password": i[1],
            "userType": 1
        })
        
if __name__ == "__main__":
    os.system("locust -f locust_canshuhua.py.py")