#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Time: 2022/3/10 9:56 上午
@Author: y
@QQ: 77386059
@Wechat: Reny-ovo-
@Description：不管用户产生速度有多慢。停留时间到了观察该用户数下的稳定状态。
"""

from collections import namedtuple
import math
import time
import random
import json
import os

from locust import HttpUser, TaskSet, task, constant, tag, between
from locust import LoadTestShape


class MyTaskSet(TaskSet):
    def on_start(self):
        # setup方法
        self.headers = {"Content-Type": "application/json"}
        self.username = "19999999999"
        self.pwd = "qwe123"

    @task  # 装饰器，说明下面是一个任务
    @tag("leave_1", "logincase")  # 标签可重复
    def login_case(self):
        url = '/authentication'  # 接口请求地址
        data = {"username": self.username, "password": self.pwd, "userType": 1}
        with self.client.post(url, data=json.dumps(data), headers=self.headers, catch_response=True,name="case_2_login") as rsp:
            # 提取响应json 的信息，定义为类变量
            # self.token = rsp.json()['token']
            # print(rsp.json())
            if rsp.json()['code'] == "0000000":
                rsp.success()
            else:
                rsp.failure("login登录失败！")

    def on_stop(self):
        # teardown方法
        pass

class WebsiteUser(HttpUser):
    # host = "http://192.168.0.60:8080"
    wait_time = between(2, 5)
    # wait_time = constant(0.5)
    tasks = [MyTaskSet]

    def __init__(self, *args, **kwargs):
        # 模拟创建用户随机等待时间
        time.sleep(random.randint(0, 5))
        super().__init__(*args, **kwargs)


Step = namedtuple("Step", ["users", "dwell"])


class StepLoadShape(LoadTestShape):
    # step参数第一个是用户总数，第二个是当前用户数持续时间
    targets_with_times = (Step(10, 10), Step(20, 15), Step(10, 10))

    def __init__(self, *args, **kwargs):
        self.step = 0
        self.time_active = False
        super().__init__(*args, **kwargs)

    def tick(self):
        if self.step >= len(self.targets_with_times):
            return None

        target = self.targets_with_times[self.step]
        users = self.get_current_user_count()

        if target.users == users:
            if not self.time_active:
                self.reset_time()
                self.time_active = True
            run_time = self.get_run_time()
            if run_time > target.dwell:
                self.step += 1
                self.time_active = False

        # 第二个参数是用户生产率，在这个模式下这个参数是无关紧要的，所以设置的尽可能高，尽快生成所需用户
        return (target.users, 100)
    
if __name__ == "__main__":
    os.system("locust -f wait_user_count.py")