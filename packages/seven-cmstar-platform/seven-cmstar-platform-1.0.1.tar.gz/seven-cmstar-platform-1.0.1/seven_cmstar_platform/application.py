# -*- coding: utf-8 -*-
"""
:Author: ChenXiaolei
:Date: 2020-04-16 14:38:22
:LastEditTime: 2021-03-02 15:58:40
:LastEditors: ChenXiaolei
:Description: 
"""

# 框架引用
from seven_framework.web_tornado.base_tornado import *
from seven_framework.web_tornado.monitor import MonitorHandler


class Application(tornado.web.Application):
    def __init__(self):
        application_settings = dict(
            # 键为template_path固定的，值为要存放HTML的文件夹名称
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            autoescape=None,
            xsrf_cookies=True)

        # cookie密钥
        cookie_secret = config.get_value("cookie_secret")
        if cookie_secret:
            application_settings["cookie_secret"] = cookie_secret

        # 第三方session组件,存储memcached或redis
        pycket = config.get_value("pycket")
        if pycket:
            application_settings["pycket"] = pycket

        handlers = []

        # 模块的路由可以独立开
        handlers.extend(self.route_handlers())

        super().__init__(handlers, **application_settings)

    def route_handlers(self):
        return [
            (r"/monitor", MonitorHandler),
        ]


def main():
    logger_info.info('application begin')
    try:
        if platform.system() == "Windows":
            import asyncio
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())

        http_server = tornado.httpserver.HTTPServer(Application(),
                                                    xheaders=True)
        # 从配置中获取启动监听端口
        http_server.listen(config.get_value("run_port"))
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        print("服务已停止运行")


if __name__ == "__main__":
    main()
