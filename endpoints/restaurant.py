
from app import app
from  helpers.db_helpers import run_query
from flask import  request, jsonify
import uuid


@app.get('/api/restaurant')
def restaurant_get():
    restaurant_list = run_query("SELECT * from restaurant")
    resp = []
    for restaurant in restaurant_list:
        rt_obj = {}
        rt_obj ['id'] = restaurant[0]
        rt_obj ['email'] = restaurant[1]
        rt_obj ['password'] = restaurant[2]
        rt_obj ['name'] = restaurant[3]
        rt_obj ['address'] = restaurant[4]
        rt_obj ['phone_number'] = restaurant[5]
        rt_obj ['bio'] = restaurant[6]
        rt_obj ['profile_url'] = restaurant[7]
        rt_obj ['banner_url'] = restaurant[8]
        rt_obj ['city'] = restaurant[9]
        resp.append(rt_obj)
    return jsonify(resp) , 200




@app.post('/api/restaurant')
def restaurant_post():
    #grabbng data
    data = request.json
    id = data.get('id')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    address = data.get('address')
    phone_number = data.get('phone_number')
    bio = data.get('bio')
    profile_url = data.get('profile_url')
    banner_url = data.get('banner_url')
    city = data.get('city')
    restaurant_id = data.get('restaurant_id')

    if not email :
        return jsonify("Missing required arguemnt : email"), 422
    if not password :
        return jsonify ("Missing required argument : password") , 422
    if not name :
        return jsonify("Missing required argument : name") , 422
    if not address :
        return jsonify("Missing required argument : address"), 422
    if not bio :
        return jsonify ("Missing required argument : bio"), 422
    if email == email and password == password:
        run_query("INSERT INTO restaurant(email, password, name, address, phone_number,bio) VALUES (?,?,?,?,?,?)" , [email, password, name, address, phone_number, bio])
        token = str(uuid.uuid4())
        run_query("INSERT into restaurant_session(token,restaurant_id)VALUES(?,?)", [token,restaurant_id])
    return jsonify ("Restaurant added"), 201

@app.patch('/api/restaurant')
def rest_patch():
    data=request.json
    id = data.get('id')
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    address = data.get('address')
    token = data.get('token')
    bio = data.get('bio')

    if password == None and token == None:
        return jsonify('Wrong password , please try again'),401

    
    result = run_query("SELECT token ,name,email,address FROM restaurant INNER JOIN restaurant_session ON restaurant_session.restaurant_id = restaurant.id WHERE email =? and token=? ",[email,token])

    if result == email or token :
        run_query("UPDATE restaurant SET password =? WHERE email =?",[password,email])
        return jsonify("password updated"),200
    if result == name or token or email:
        run_query("UPDATE restaurant SET name = ? WHERE email =?",[name,email])
        return jsonify("name updated"),200
    


    # if result == name or token:
    #     run_query("UPDATE restaurant SET name=? WHERE email=? ")
    #     return jsonify("name updated"),200
    
    
# if bio != None and token !=None:
    #     run_query("UPDATE client SET bio = ? WHERE id =(SELECT client_id FROM client_session WHERE token = ?" , [bio, token])
    #     return jsonify('bio updated')





