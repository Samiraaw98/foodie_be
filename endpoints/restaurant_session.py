from helpers.db_helpers import run_query
from app import app
from flask import  jsonify , request
from flask_cors import CORS
import sys
import uuid



@app.post('/api/restaurant-login')
def rest_login():
    data=request.json
    email = data.get('email')
    password =data.get('password')

    if email !=None and password !=None:
        run_query('SELECT * FROM restaurant WHERE email = ? and password = ?', [email,password])
    if email =='email' and password =='password':
        token= ""
        run_query("INSERT INTO restaurant_session(token) VALUES(?)", [token])
        return jsonify('success'), 200
    else:
        email != 'email' and password !='password'
        return jsonify("Invalid entry"), 401

@app.delete('/api/restaurant-login')
def rest_delete():
    data = request.json
    token = data.get('token')
    if token != None:
        run_query("DELETE FROM restaurant_session WHERE token=?", [token])
    return jsonify ('user deleted'), 200


