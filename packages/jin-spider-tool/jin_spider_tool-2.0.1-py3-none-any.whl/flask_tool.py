# -*- coding:utf-8 -*-
# !/usr/bin python3                                 
# encoding    :   -*- utf-8 -*-                            
# @author     :    None                             
# @software   :   PyCharm      
# @file       :   flask_tool.py
# @Time       :   2021/9/1 7:27 下午
import flask
from kazoo.client import KazooClient
import sys
import os
import time
import json
import traceback
import logging

number_function_calls = 0


class SpiderAssistant(object):

    def __init__(self, original_method, login_method):
        self.login_method = login_method
        self.original_method = original_method
        a = traceback.extract_stack()[-2]
        sys.path.append(a[0])
        self.org_path = a[0]
        self.app = flask.Flask(__name__)

        # self.app.debug = True  # 创建1个Flask实例

        @self.app.route('/')  # 路由系统生成 视图对应url,1. decorator=app.route() 2. decorator(first_flask)
        def first_flask():  # 视图函数
            return 'Hello World'  # response

        @self.app.route('/heartbeat')  # 路由系统生成 视图对应url,1. decorator=app.route() 2. decorator(first_flask)
        def the_heartbeat():  # 视图函数
            return 'Hello World'  # response

        @self.app.route('/spider', methods=['POST'])
        def post_data():
            global number_function_calls
            data = flask.request.json
            if data:
                number_function_calls += 1
                result = self.original_method(data)
                number_function_calls -= 1
                if result and "code" in result and result['code'] is not None and "msg" in result:
                    return flask.jsonify({
                        "code": result["code"],
                        "msg": result["msg"],
                        "data": result
                    })
                else:
                    return flask.jsonify({
                        "code": 999,
                        "msg": "未知异常",
                        "data": None
                    })
            else:
                return flask.jsonify({
                    "code": 999,
                    "msg": "没有传入数据",
                    "data": None
                })

        @self.app.route('/login', methods=['POST'])
        def login_api():
            data = flask.request.json
            if data:
                result = self.login_method(data)
                if result and "code" in result and result['code'] is not None and "msg" in result:
                    return flask.jsonify({
                        "code": result["code"],
                        "msg": result["msg"],
                        "data": result
                    })
                else:
                    return flask.jsonify({
                        "code": 999,
                        "msg": "未知异常",
                        "data": None
                    })
            else:
                return flask.jsonify({
                    "code": 999,
                    "msg": "没有传入数据",
                    "data": None
                })

    def __call__(self):
        self.original_method()

    def flask_tool_api(self, *args, **kwargs):

        self.app.run(*args, **kwargs)  # 启动socket


class ZKClient(object):

    def __init__(self, hosts, setting_file="gunicorn_mooc"):
        self.setting_file = setting_file
        a = traceback.extract_stack()[-2]
        sys.path.append(a[0])
        self.org_path = a[0]
        self._zk = KazooClient(hosts=hosts)
        self._zk.start()

    def zookeeper_register(self, path, value_data: dict):
        """
        path：          节点路径
        value：         节点对应的值，注意值的类型是 bytes
        ephemeral： 若为 True 则创建一个临时节点，session 中断后自动删除该节点。默认 False
        sequence:     若为 True 则在你创建节点名后面增加10位数字（例如：你创建一个 testplatform/test 节点，实际创建的是 testplatform/test0000000003，这串数字是顺序递增的）。默认 False
        makepath：  若为 False 父节点不存在时抛 NoNodeError。若为 True 父节点不存在则创建父节点。默认 False
        """
        # field_list = ["ipAddr", "port", "spiderName", "websiteId"]
        field_list = []
        # if "spiderName" not in value_data:
        #     # 获取调用者
        #     value_data["spiderName"] = traceback.extract_stack()[-2][2]
        # if "ipAddr" not in value_data:
        #     # 获取本机ip
        #     value_data["ipAddr"] = self.get_host_ip()

        # print(value_data['spiderName'])
        # print(list(value_data.values()))

        if field_list != list(value_data.keys()):
            try:
                # 创建节点：makepath 设置为 True ，父节点不存在则创建，其他参数不填均为默认
                self._zk.create(path=path, value=json.dumps(value_data).encode(), ephemeral=True, makepath=True)
                # 操作完后，别忘了关闭zk连接
                logging.info("注册成功")
                return "ok"
            except Exception as e:
                # print(traceback.format_exc().split('\n')[-2])
                if traceback.format_exc().split('\n')[-2] != "kazoo.exceptions.NodeExistsError":
                    logging.exception(e)
                # else:
                #     self._zk.set(path, json.dumps(value_data).encode(), version=-1)

                return traceback.format_exc().split('\n')[-2]
        else:
            return 1

    def zookeeper_delete(self, path):
        """
        参数 recursive：若为 False，当需要删除的节点存在子节点，会抛异常 NotEmptyError 。若为True，则删除 此节点 以及 删除该节点的所有子节点
        删除节点对应的value
        """
        try:
            global number_function_calls
            while 1:
                if number_function_calls == 0:
                    time.sleep(1)
                    self._zk.delete(path, recursive=False)
                    time.sleep(1)
                    break
                else:
                    time.sleep(1)
            str_pop = "{print $2}"
            os.popen(f"kill -9 `ps -ef | grep {self.setting_file} | awk '{str_pop}'`")
            os.popen(f"kill -9 `ps -ef | grep {self.org_path} | awk '{str_pop}'`")

            return "del"
        except Exception as e:
            logging.exception(e)
            return traceback.format_exc().split('\n')[-2]

    def zookeeper_close(self):
        # 操作完后，关闭zk连接
        try:
            global number_function_calls
            while 1:
                if number_function_calls == 0:
                    time.sleep(1)
                    self._zk.stop()
                    time.sleep(1)
                    break
                else:
                    time.sleep(1)
            str_pop = "{print $2}"
            os.popen(f"kill -9 `ps -ef | grep {self.setting_file} | awk '{str_pop}'`")
            os.popen(f"kill -9 `ps -ef | grep {self.org_path} | awk '{str_pop}'`")
            return "close"
        except Exception as e:
            logging.exception(e)
            return traceback.format_exc().split('\n')[-2]
