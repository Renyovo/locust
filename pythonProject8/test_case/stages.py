#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Time: 2022/3/10 9:56 上午
@Author: y
@QQ: 77386059
@Wechat: Reny-ovo-
@Description: 模拟不同阶段，有不同的用户总数以及用户产生速率
"""

import json, os
from locust import HttpUser, TaskSet, task, constant, between, tag
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


class StagesShape(LoadTestShape):
    """
        ps:在不同的阶段 具有不同的用户数和 产生率的 图形形状
        duration -- 持续时间经过多少秒后，进入到下个阶段
        users -- 总用户数
        spawn_rate -- 产生率，即每秒启动/停止的用户数
    """

    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 10},
        {"duration": 100, "users": 50, "spawn_rate": 10},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 220, "users": 30, "spawn_rate": 10},
        {"duration": 230, "users": 10, "spawn_rate": 10},
        {"duration": 240, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
    
if __name__ == "__main__":
    os.system("locust -f stages.py")