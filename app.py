import os
from flask import *
import pymysql
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
jwt = JWTManager(app)

CORS(app)
cors = CORS(app, resources={
    r"/gym/*": {
        "origins": "*"
    }
})


@app.route('/gym/clients', methods=['GET'])
def clients():
    try:
        con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
        sql = "select * from client_table order by reg_date ASC"
        # cannot use sql injection
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            response = jsonify({'error': 'Not found'})
            response.status_code = 404
            return response
        else:
            rows = cursor.fetchall()
            response = jsonify(rows)
            response.status_code = 200
            return response
    except:
        response = jsonify({'error': 'Server error'})
        response.status_code = 400
        return response


@app.route('/gym/token', methods=['POST'])
def create_token():
    json = request.json
    phone = json['phoneno']
    password = json['password']
    # connecting to the database

    if phone != "123" or password != "test":
        return jsonify({'msg', "usename or pass is not correct"}), 401

    access_token = create_access_token(identity=phone)
    return jsonify(access_token=access_token)


@app.route('/gym/login', methods=['POST'])
def login():
    json = request.json
    phone = json['username']
    password = json['password']
    # connecting to the database

    con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
    sql = "select * from users_table where phone_no = %s"
    # cannot use sql injection
    cursor = con.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, (phone))

    # check rows returned
    if cursor.rowcount == 0:
        response = jsonify({'error': 'Phone does not exist'})
        response.status_code = 404
        return response
    else:
        row = cursor.fetchone()
        # password is index 5, email index 8 ,phone index 9

        from functions import verify_password, send_sms, send_email, otp_gen
        status = verify_password(row['password'], password)
        if status:
            response = jsonify({'result': row})
            response.status_code = 200
            return response
        else:
            response = jsonify({'error': 'wrong credentials'})
            response.status_code = 404
            return response


# deleting client from table
@app.route('/gym/deleteclients/<client_id>', methods=['DELETE'])
def del_client(client_id):
    try:
        con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
        sql = "delete from client_table where client_id = %s"
        cursor = con.cursor()
        cursor.execute(sql, (client_id))
        con.commit()
        count = cursor.rowcount
        print(count)
        if count == 0:
            response = jsonify({'error': 'Client not deleted'})
            response.status_code = 203
            return response
        else:
            response = jsonify({'success': 'Client deleted successfully'})
            response.status_code = 200
            return response
    except:
        response = jsonify({'error': 'Client not deleted'})
        response.status_code = 700
        return response


@app.route('/gym/kin', methods=['GET'])
def kin():
    try:
        con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
        sql = "select * from kin_table order by reg_date ASC"
        # cannot use sql injection
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            response = jsonify({'error': 'Not found'})
            response.status_code = 404
            return response
        else:
            rows = cursor.fetchall()
            response = jsonify(rows)
            response.status_code = 200
            return response
    except:
        response = jsonify({'error': 'Server error'})
        response.status_code = 400
        return response


# adding a relative
@app.route('/gym/addkin', methods=['POST'])
def addkin():
    json = request.json
    first_name = json['firstName']
    last_name = json['lastName']
    id_no = json['idno']
    phone_no = json['phoneno']
    kin_id = json['value']

    if len(first_name) == 0:
        response = jsonify({'code': 1, "msg": 'firstname is Empty'})
        response.status_code = 400
        return response

    elif len(last_name) == 0:
        response = jsonify({'code': 2, "msg": 'last_name is Empty'})
        response.status_code = 400
        return response
    elif len(id_no) == 0:
        response = jsonify({'code': 3, "msg": 'id number is Empty'})
        response.status_code = 400
        return response
    elif len(phone_no) == 0:
        response = jsonify({'code': 4, "msg": 'phone number is Empty'})
        response.status_code = 400
        return response

    else:
        con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
        sql = "insert into relative_table(first_name,last_name, id_no, phone_no,kin_id) values(%s,%s,%s,%s,%s)"
        cursor = con.cursor()
        cursor.execute(sql, (first_name, last_name, id_no, phone_no, kin_id))
        con.commit()
        response = jsonify({'success': 'Relative added'})
        response.status_code = 200
        return response


# fetching all the relatives
@app.route('/gym/addedkin', methods=['GET'])
def addedkin():
    try:
        con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
        sql = "select * from relative_table order by reg_date ASC"
        # cannot use sql injection
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            response = jsonify({'error': 'Not found'})
            response.status_code = 404
            return response
        else:
            rows = cursor.fetchall()
            response = jsonify(rows)
            response.status_code = 200
            return response
    except:
        response = jsonify({'error': 'Server error'})
        response.status_code = 400
        return response


# fetching the membership types
@app.route('/gym/memberships', methods=['GET'])
def memberships():
    try:
        con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
        sql = "select * from membership_table order by reg_date ASC"
        # cannot use sql injection
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)

        if cursor.rowcount == 0:
            response = jsonify({'error': 'Not found'})
            response.status_code = 404
            return response
        else:
            rows = cursor.fetchall()
            response = jsonify(rows)
            response.status_code = 200
            return response
    except:
        response = jsonify({'error': 'Server error'})
        response.status_code = 400
        return response


# adding a a member
@app.route('/gym/addmember', methods=['POST'])
def addmember():
    json = request.json
    first_name = json['firstName']
    last_name = json['lastName']
    id_no = json['idno']
    phone_no = json['phoneno']
    status = json['status']
    membership_id = json['valzue']
    relative_id = json['value']
    gender = json['gender']

    if len(first_name) == 0:
        response = jsonify({'code': 1, "msg": 'firstname is Empty'})
        response.status_code = 400
        return response

    elif len(last_name) == 0:
        response = jsonify({'code': 2, "msg": 'last_name is Empty'})
        response.status_code = 400
        return response
    elif len(id_no) == 0:
        response = jsonify({'code': 3, "msg": 'id number is Empty'})
        response.status_code = 400
        return response

    elif len(phone_no) == 0:
        response = jsonify({'code': 4, "msg": 'phone number is Empty'})
        response.status_code = 400
        return response
    elif len(gender) == 0:
        response = jsonify({'code': 2, "msg": 'gender is Empty'})
        response.status_code = 400
        return response
    else:
        con = pymysql.connect(host='localhost', user='root', password='', database='gym_db')
        sql = "insert into client_table(first_name,last_name, id_no, phone_no,membership_id,status,relative_id," \
              "gender) values(%s,%s,%s,%s,%s,%s,%s,%s) "
        cursor = con.cursor()
        cursor.execute(sql, (first_name, last_name, id_no, phone_no, membership_id, status, relative_id, gender))
        con.commit()
        response = jsonify({'success': 'Member added'})
        response.status_code = 200
        return response


@app.route('/gym/addrequest', methods=['POST'])
def requests():
    json = request.json
    request_name = json['title']
    request_subject = json['body']

    if len(request_name) == 0:
        response = jsonify({'code': 1, "msg": 'firstname is Empty'})
        response.status_code = 400
        return response

    elif len(request_subject) == 0:
        response = jsonify({'code': 2, "msg": 'last_name is Empty'})
        response.status_code = 400
        return response

    else:
        con = pymysql.connect(host='localhost', user='root', password='', database='challenge_db')
        sql = "insert into requests(request_name,request_subject) values(%s,%s)"
        cursor = con.cursor()
        cursor.execute(sql, (request_name, request_subject))
        con.commit()
        response = jsonify({'success': 'Request added'})
        response.status_code = 200
        return response


if __name__ == '__main__':
    app.run(debug=True, port=8000)
