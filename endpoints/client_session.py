import uuid
from app import app
from helpers.db_helpers import run_query
from flask import  request, jsonify
from flask_cors import CORS 
import sys
# token generator: (import uuid)



CORS(app)

@app.post('/api/client-login')
def user_post():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email !=None and password!= None:
           run_query("SELECT * FROM client WHERE email=? and password=?" , [email,password])
    if email == email  and password == password:
        token="slkjdlksj356"
        run_query("INSERT INTO client_session(token) VALUES (?) ",[ token ])
        return jsonify ("success"),200
    if email != email and password != password:
        return jsonify("Invalid entry, user may not exist"),401


@app.delete('/api/client-login')
def user_delete():
    data = request.json
    token = data.get('token')
    if token != None:
        run_query("DELETE FROM client_session WHERE token=?" , [token])
    return jsonify ("logged out") ,200



