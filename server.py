import tornado.ioloop
import tornado.web
from main import Talker
def paramsfromrequest(request):
    """Changes the format of the HTTP request parameters so that they may be more easily used"""
    params = request.arguments
    params_dict = {}
    for key, value in request.arguments.items():
        if len(value) == 1:
            params_dict[key] = value[0].decode('UTF-8')
        else:
            params_dict[key] = []
            for part in value:
                params_dict[key].append(part.decode('UTF-8'))
    return params_dict

talker = Talker()

class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.params = paramsfromrequest(self.request)
    def get(self):
        try:
            self.write(talker.speak(self.params["text"]))
        except KeyError:
            self.write("GET a string under the parameter of 'text', please")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
