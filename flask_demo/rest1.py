from flask import Flask, jsonify, request
from datetime import datetime
import mariadb
import json
import uuid

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/health-check')
def health_check():
    return "Server is running on 5000 port"  

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'mysql',
    'database': 'mydb'
}

@app.route('/users')
def users():
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute("select id, user_id, pwd from users")

    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    # return json.dumps(json_data)
    return jsonify(json_data)   

@app.route('/users/<userId>')
def users_detail(userId):
    # return "{\"name\":%s}" % (userId)
    return jsonify({"user_id": userId})

@app.route('/users', methods = ['POST'])
def userAdd():
    user = request.get_json()
    user['user_id'] = uuid.uuid4() #uuid1() ~ uuid5()
    user['created_at'] = datetime.today()
    # db에 추가
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql = "INSERT INTO users (user_id, pwd) VALUES(%s, %s)"
    val = (user['name'], user['pwd'])

    cur.execute(sql, val)
    conn.commit()

    # kafka에 전송 (topic에만 전송)
    # 200 OK -> 201 Created 
    return jsonify(user), 201

if __name__ == "__main__":
    app.run()