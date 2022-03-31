.
├── README.md  
├── __pycache__  
├── common                       //配置文件目录。
│   ├── __init__.py
│   └── config.py                //配置文件路径  
├── list.txt  
├── locust.conf                  //locust参数配置文件  
├── date                          //数据文件目录  
│   └── test.csv                 //数据文件  
├── log                          //日志存放目录  
│   └── locust.log               //locust日志  
├── requirements                 //所需安装环境目录  
│   └── requirements.txt         //所需安装环境  
├── static                       //web-UI扩展  
│   └── extend.js  
├── templates                    //web-UI扩展  
│   └── extend.html  
└── test_case                    //性能测试脚本目录  
    ├── __init__.py  
    ├── __pycache__  
    ├── double_wave.py           //双波形负载测试  
    ├── locust_canshuhua.py      //参数化接口入参   
    ├── locust_test.py           //正常性能测试  
    ├── stages.py                //时间阶段负载测试  
    ├── step_load.py             //逐步负载测试  
    ├── time_peak.py             //时间峰值负载测试  
    └── wait_user_count.py       //用户数稳定负载测试  

9 directories, 18 files


环境配置：pip install locust

脚本运行方式：
1. 【正常脚本运行】终端运行  locust -f 文件名                    //按文件名执行
2. 【指定被测服务器ip】终端运行  locust -f 文件名 -H 127.0.0.1       //指定被测服务器ip（可在web端进行修改）
3. 【指定本机端口】终端运行  locust -f 文件名 -P 9999            //指定本定访问的端口号（localhost:9999）,默认8089
4. 【no-web模式】终端运行  locust -f 文件名 --headless -u/--users 100 -t 60 --host=127.0.0.1:8080  --csv=data          //--headless为no-web测试，结果直接在终端展示，一定要指定-u用户数，-t测试时间单位：s，--host被测服务器ip，还可以指定生产csv文件前缀（--csv如果不写，则不会生成csv文件，如果写的话执行测试之后会在当前文件目录生产测试结果的csv文件，执行--headless时除了csv参数可选择填写，其他参数必须填写）
5. 【分布式】主机终端运行  locust -f 文件名 --master，负载机终端运行  locust -f 文件名 --worker --master-host 127.0.0.1（主机ip） --master-port 5557（默认5557可不写）（不同机器网络要互通）
6. 【指定标签执行】终端运行  locust -f 文件名 -T 标签名 按标签去执行用例（执行标签为所输入标签名的用例），locust -f 文件名 -E 标签名 执行除了所输入标签的所有用例（一个用例可以同时有多个标签名，不同用例之间标签名可重复）
7. 【根据配置文件运行】终端运行  locust --config=配置文件名        //按照配置文件运行脚本，脚本路径以及其他参数信息可在配置文件中指定

注：运行脚本时要注意当前所处文件目录，可使用文件绝对路径运行脚本

帮助：locust -h/--help

脚本扩展：
locust源码github地址：https://github.com/locustio/locust
locust官方参考文档：http://docs.locust.io/en/stable/
locust参数配置文件及扩展：https://blog.csdn.net/u012002125/article/details/112871989?spm=1001.2014.3001.5502
