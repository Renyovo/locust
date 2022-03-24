#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Time: 2022/3/10 9:57 上午
@Author: y
@QQ: 77386059
@Wechat: Reny-ovo-
@Description: 设置整个压测时间，以及用户产生率
"""
import random, json, datetime, os
from locust import SequentialTaskSet, HttpUser, between, task, tag, LoadTestShape, constant


class TaskSuit(SequentialTaskSet):
    # 类继承SequentialTaskSet 或 TaskSet类
    # 当类里面的任务请求有先后顺序时，继承SequentialTaskSet类
    # 没有先后顺序，可以使用继承TaskSet类
    # setup方法
    def on_start(self):
        self.headers = {"Content-Type": "application/json"}
        self.username = "19999999999"
        self.pwd = "qwe123"

    @task  # 装饰器，说明下面是一个任务
    @tag("leave_1", "logincase")  # 标签可重复
    def login_case(self):
        url = '/authentication'  # 接口请求地址
        data = {"username": self.username, "password": self.pwd, "userType": 1}
        with self.client.post(url, data=json.dumps(data), headers=self.headers, catch_response=True,
                            name="case_2_login") as rsp:
            if rsp.json()['code'] == "0000000":
                rsp.success()
            else:
                rsp.failure("login登录失败！")

    def on_stop(self):
        # teardown方法
        pass
    

class TaskPlan(HttpUser):
    # task_set属性已经被移除，tasks属性值必须为列表或字典
    tasks = [TaskSuit]
    wait_time = between(0.01, 3)



class MyCustomShape(LoadTestShape):
    # time_limit设置时限整个压测过程为60秒
    time_limit = 60
    # 设置产生率一次启动10个用户
    spawn_rate = 10
    
    def tick(self):
        '''
        设置tick()函数
        并在tick()里面调用 get_run_time()方法
        '''
        # 调用get_run_time()方法获取压测执行的时间
        run_time = self.get_run_time()
        
        # 运行时间在time_limit之内则继续执行
        if run_time < self.time_limit:
            # user_count计算每10秒钟增加10个
            # -1为每10秒增加10个用户，-2为每100秒增加100个用户，-3为每1000秒增加1000用户
            user_count = round(run_time, -1)
            print(str(user_count) + ">>>>>" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"))
            return (user_count,self.spawn_rate)
        return None
    
if __name__ == "__main__":
    os.system("locust -f time_peak.py")


# 终端-f -H -P
# --step-load --step-users --step-time
# --headless -u/--users 用户数 -t 时间 --host=  --csv=
# --master --worker  (--worker --master-host 127.0.0.1（主机ip） --master-port 5557（默认5557可不写）（不同机器网络要互通）)
# -T 标签名 按标签去执行用例 -E 标签名 执行除了所输入标签的所有用例
