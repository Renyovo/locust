#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Time: 2022/3/10 9:55 上午
@Author: y
@QQ: 77386059
@Wechat: Reny-ovo-
@Description: 双峰，在1/3和2/3处模拟两个峰值
"""

import math, json, os
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


class DoubleWave(LoadTestShape):
    '''
    自定义一个双波形图形，
    模拟在某两个时间点的最高值


    参数解析:
        min_users ： 最小用户数
        peak_one_users ： 用户在第一个峰值
        peak_two_users ： 用户在第二个峰值
        time_limit ： 测试执行总时间


    '''
    min_users = 20
    peak_one_users = 60
    peak_two_users = 40
    time_limit = 600

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                (self.peak_one_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                + (self.peak_two_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                + self.min_users
            )
            return (round(user_count), round(user_count))
        else:
            return None
        
if __name__ == "__main__":
    os.system("locust -f double_wave.py")