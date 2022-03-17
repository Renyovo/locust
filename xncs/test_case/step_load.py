#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Time: 2022/3/10 9:56 上午
@Author: y
@QQ: 77386059
@Wechat: Reny-ovo-
@Description: 逐步负载，每隔多少秒新增多少用户
"""

import math, os, json
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


class StepLoadShape(LoadTestShape):
    '''
        step_time -- 逐步加载时间长度
        step_load -- 用户每一步增加的量
        spawn_rate -- 用户在每一步的停止/启动的多少用户数
        time_limit -- 时间限制压测的执行时长
    '''

    # 逐步负载策略每隔30秒新增启动10个用户
    step_time = 30
    step_load = 10
    spawn_rate = 10
    time_limit = 600

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)
    
if __name__ == "__main__":
    os.system("locust -f step_load.py")