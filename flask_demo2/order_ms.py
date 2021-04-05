import flask
from flask import Flask, jsonify, request
from flask_restful import reqparse
from datetime import datetime

import flask_restful
import mariadb
import json
import uuid

app = Flask(__name__)
app.config["DEBUG"] = True
api = flask_restful.Api(app)

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'mysql',
    'database': 'mydb'
}

@app.route('/order-ms')
def index():
    return "Welcome to ORDER Microservice!"

class Order(flask_restful.Resource):
    def get(self, user_id):
        conn = mariadb.connect(**config)
        cursor = conn.cursor()
        sql = "select * from orders where user_id=? order by id desc"
        cursor.execute(sql, [user_id])
        result_set = cursor.fetchall()

        json_data = []
        for result in result_set:
            json_data.append(result)

        return jsonify(json_data)

    def post(self, user_id):
        json_data = request.get_json()
        json_data['user_id'] = user_id
        json_data['order_id'] = str(uuid.uuid4()) 
        json_data['ordered_at'] = str(datetime.today())

        # DB insert
        response = jsonify(json_data)
        response.status_code = 200 
        
        return response

class OrderDetail(flask_restful.Resource):
    def get(self, user_id, order_id):
        return {'user_id': user_id, 'order_id': order_id}

api.add_resource(Order, '/order-ms/<string:user_id>/orders')
api.add_resource(OrderDetail, '/order-ms/<string:user_id>/orders/<string:order_id>')

if __name__ == '__main__':
    app.run()
