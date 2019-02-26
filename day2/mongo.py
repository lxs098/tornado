#Author:lixiaosong
#@Time:2019/2/26 0026 8:48
import os
from pymongo import MongoClient
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
from tornado.options import define,options
define('port', default=8000, help='run on the given port',type=int)
#链接mongodb数据库
MONGODB_DB_URL = os.environ.get('OPENSHIFT_MONGODB_DB_URL') if os.environ.get(
    'OPENSHIFT_MONGODB_DB_URL') else 'mongodb://localhost:27017/'

#重写Application方法，因为所有url调用都会经过application方法
class Application(tornado.web.Application):
    def __init__(self):
        #方法被调用时编辑路由，链接数据库，还有静态文件的路径配置
        handlers = [
            (r'/', IndexHandler),
            (r'/poem', PoemHandler),
            (r'/delete/(\d+)', DeleteHandler),
        ]
        #静态文件路径
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), "static")
        )
        # mongodb数据库连接
        client = MongoClient(MONGODB_DB_URL)
        self.db = client['tornado']
        #调用父类__init__方法
        tornado.web.Application.__init__(self,handlers,**settings)

#首页展示
class IndexHandler(tornado.web.RequestHandler):
    # mongodb数据库读取
    def get(self):
        attr = []
        for i in self.application.db.widgets.find():
            attr.append(i)
        self.render('index.html',attr=attr)
#数据库保存
j = 0
class PoemHandler(tornado.web.RequestHandler):
    def post(self):
        #mongodb数据库自动生成的objectid不能被作为值传给templates，所以重写id
        #j作为数据存储的唯一id，这样在数据删除时会很方便
        global j
        j += 1
        # 获取输入内容
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        noun3 = self.get_argument('noun3')
        verb = self.get_argument('verb')
        body = {
            'noun1': noun1,
            'noun2': noun2,
            'noun3': noun3,
            'verb': verb,
            '_id':j
        }
        #储存mongodb数据库
        self.application.db.widgets.insert(body)
        #接口数据，
        self.write(body)

#删除
class DeleteHandler(tornado.web.RequestHandler):
    #def delete方法不能用，只能采用get方式来删除某一条数据
    def get(self,id):
        self.application.db.widgets.remove({'_id':int(id)})
        self.write('删除成功')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
