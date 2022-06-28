
from app import app 
from helpers.db_helpers import run_query
from flask import  request, jsonify
import uuid

@app.get('/api/client')
def client_get():
    client_list = run_query("SELECT * from client")
    resp = []
    for client in client_list:
        cl_obj = {}
        cl_obj['id'] = client[0]
        cl_obj ['email'] = client[1]
        cl_obj ['username'] = client[2]
        cl_obj ['password'] = client[3]
        cl_obj ['first_name'] = client[4]
        cl_obj ['last_name'] = client[5]
        cl_obj ['createdAt'] = client[6]
        cl_obj ['pictureUrl'] = client[7]
        resp.append(cl_obj)
    return jsonify(resp) , 200

@app.post('/api/client')
def client_post():
    # grabbing data
    data = request.json
    id = data.get('id')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    picture_url = data.get('pictureUrl')
    client_id = data.get('client_id')


    if not email :
        return jsonify("Missing required arguemnt : email"), 422
    if not username:
        return jsonify("Missing required argument : username"), 422
    if not password :
        return jsonify ("Missing required argument : password") , 422
    if not first_name:
        return jsonify ("Missing required argument : first name") , 422

    if email==None or password == None:
        return jsonify("Missing email/password , user may not exist"),400
    if email != None and password !=None:
        run_query("INSERT INTO client (id,email, username, password, first_name, last_name, picture_url) VALUES (?,?,?,?,?,?,?)", [id,email, username, password, first_name, last_name,picture_url])
        token = str(uuid.uuid4())
        run_query("INSERT INTO client_session(token , client_id) VALUES (?,?)", [token, client_id])
    return jsonify ("Client added") , 201      
    
@app.patch('/api/client')
def client_patch():
        data = request.json
        id = data.get('id')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        token = data.get('token')
        picture_url = data.get('pictureUrl')
        bio = data.get('bio')

        if password == None and token == None:
            return jsonify("Wrong password, please try again"),401

        result = run_query("SELECT token,first_name ,last_name, ,  email,password ,picture_url FROM client INNER JOIN client_session ON client_session.client_id = client.id WHERE email=? and token=?" , [email, token])
        if result ==  email  or token:
            run_query("UPDATE client SET password = ? WHERE email = ?" , [password,email])
            return jsonify("password updated"),200

        if result == username  or token :
            run_query("UPDATE client SET username=? WHERE email=?",[username,email])
            return jsonify("username updated"), 200

        if result == first_name or token:
            run_query("UPDATE client SET first_name =? WHERE email =?", [first_name,email])
            return jsonify("firstName updated"),200
        if result == last_name or token:
            run_query("UPDATE client SET last_name=? WHERE email = ?", [last_name,email])
            return jsonify("last name updated"),200
        if result == picture_url or token:
            run_query("UPDATE client SET picture_url WHERE email= ?", [picture_url,email])
            return jsonify("picture updated"),200

@app.delete('/api/client')
def client_delete():
    data=request.json
    password=data.get('password')
    email = data.get('email')
    token = data.get('token')
    id = data.get('id')
    client_id = data.get('client_id')

    if email == None or password == None:
        return jsonify("Missing email/password"), 400

    result = run_query("SELECT client_id,token,email FROM client INNER JOIN client_session ON client_session.client_id = client.id WHERE email =? and token=? ", [email,token])
    if result == email or token :
        run_query("DELETE FROM client_session WHERE token =?", [token])
        run_query("DELETE FROM client WHERE email =? ", [email])
        return jsonify("Client deleted"), 200


    


