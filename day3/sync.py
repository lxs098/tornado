#Author:lixiaosong
#@Time:2019/2/27 0027 10:51
import tornado.web
import os
from tornado.websocket import WebSocketHandler
import tornado.options
import tornado.ioloop
import tornado.httpserver
from tornado.options import define,options
define('port', default=8000, help='run on the given port',type=int)
class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r'/', IndexWebSocketHandler),
            (r'/chat', ChatWebSocketHandler),
        ]
        #静态文件路径
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self,handlers,**settings)
class IndexWebSocketHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')
class ChatWebSocketHandler(WebSocketHandler):
    users = []
    def open(self):
        print(self)
        self.users.append(self)
        for user in self.users:
            user.write_message('[{{}}]登录了'.format(self.request.remote_ip))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

