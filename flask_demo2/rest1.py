from flask import Flask, jsonify
import flask_restful
from flask_restful import reqparse
import time
import consul

app = Flask(__name__)
# app.config["DEBUG"] = True
# $ flask app  <- app.py
# 실행 파일을 변경하려면, set FLASK_APP=new_file.py
# 디버그 모드 실행, set FLASK_DEBUG=True -> auto refresh

api = flask_restful.Api(app)

def multiply(param1, param2):
    return param1 * param2

@app.route('/healthcheck')
def health_check():
    return 'OK', 200

@app.route('/')
def index():
    return "Hello, Flask!"

class HelloWorld(flask_restful.Resource):
    def get(self):
        parser = reqparse.RequestParser()

        # Query String
        # GET /api/multiply?param1=3&param2=4 -> 12
        parser.add_argument('param1')
        parser.add_argument('param2')
        args = parser.parse_args()

        param1 = args['param1']
        param2 = args['param2']

        if (not param1) or (not param2):
            return {
                'state': 0,
                'response': None
            }

        param1 = int(param1)
        param2 = int(param2)

        result = multiply(param1, param2)
        return {
            'state': 1,
            'response': result
        } 

api.add_resource(HelloWorld, '/api/multiply')

if __name__ == '__main__':
    service_name = 'my_multiply'
    consul = consul.Consul()
    consul.agent.service.register(service_name)

    time.sleep(80 / 1000.0)
    index, nodes = consul.health.service(service_name)
    print(index)
    print(nodes)
    print("*" * 10)

    app.run(port=8000)

