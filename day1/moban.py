#Author:lixiaosong
#@Time:2019/2/25 0025 13:54
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        #模板渲染
        self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        #获取input表单name属性
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        #渲染到poem页面
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                difference=noun3)

#模板控制语句
class BookHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "book.html",
            title="Home Page",
            header="Books that are great",
            #book.html模板循环
            books=[
                "Learning Python",
                "Programming Collective Intelligence",
                "Restful Web Services"
            ]
        )
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/poem', PoemPageHandler),
            (r'/book',BookHandler),
        ],
        #当前路径templates
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()