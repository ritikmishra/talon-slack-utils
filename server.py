import tornado.ioloop
import tornado.web
from main import Talker
import os
# url = "https"
try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = 8888

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
        self.resjson = {"response_type":"in_channel"}
        self.words = []
        try:
            for word in self.params['text']:
                if (not word[0] == "<") and (not word[-1] == ">"):
                    self.words.append(word)
            self.words = " ".join(self.words)
        except KeyError:
            self.words = " "
        self.add_header("Content-type", "application/json")
    def post(self):
        self.resjson['text'] = talker.speak(self.words)
        self.write(self.resjson)
    def get(self):
        self.resjson['text'] = talker.speak(self.words)
        self.write(self.resjson)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    print("Listening on port " + str(PORT))
    tornado.ioloop.IOLoop.current().start()
