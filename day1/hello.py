#Author:lixiaosong
#@Time:2019/2/25 0025 11:30
import textwrap
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
#端口号     默认8000  可以运行时定义端口号      int类型
define("port", default=8000, help="run on the given port", type=int)
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        #get传参如?greeting=，如果没有设置参数，则第二个参数作为默认参数
        greeting = self.get_argument('greeting', 'Hello')
        #http响应信息
        self.write(greeting + ', friendly user!')

class ReverseHandler(tornado.web.RequestHandler):
    #url正则传参，列表形式
    def get(self, input):
        self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        #post传参，text作为键
        text = self.get_argument('text')
        #获取的字体大小
        width = self.get_argument('width', 40)
        #设置字体大小
        self.write(textwrap.fill(text, int(width)))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    #url请求路径，使用正则来按指定路径，访问类
    app = tornado.web.Application(handlers=[
        (r"/", IndexHandler),
        (r"/reverse/(\w+)", ReverseHandler),
        (r"/wrap", WrapHandler)
    ])
    #启动tornado
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

