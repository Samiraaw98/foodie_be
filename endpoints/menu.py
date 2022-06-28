from cProfile import run
from helpers.db_helpers import run_query
from app import app
from flask import  request, jsonify





@app.get('/api/menu')
def menu_get():
    menu_list = run_query("SELECT * from menu_item")
    resp = []
    for menu in menu_list:
        an_obj = {}
        an_obj ['id'] = menu[0]
        an_obj ['name'] = menu[1]
        an_obj ['description'] = menu[2]
        an_obj ['price'] = menu[3]
        an_obj ['image_url'] = menu[4]
        an_obj ['restaurant_id'] = menu[5]
        resp.append(an_obj)
    return jsonify(resp), 200


@app.post('/api/menu')
def menu_post():
    data=request.json
    id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    image_url = data.get('image_url')
    restaurant_id = data.get('restaurant_id')
    token = data.get('token')

    if not name :
        return jsonify ("Missing required argument : name"), 401
    if not price :
        return jsonify ("Missing required argument : price"), 422
    run_query("INSERT INTO menu_item(name, description, price , image_url) VALUES (?,?,?,?)" ,[name, description, price, image_url])
    return jsonify ("menu item added!"), 201

@app.patch('/api/menu')
def menu_patch():
    data=request.json
    id = data.get('id')
    name = data.get('name')
    token = data.get('token')
    if id != "" and id != None and name != "" and name != None:
        run_query("UPDATE menu_item SET name = ? WHERE id = (SELECT id FROM restaurant_session WHERE token = ?)" , [name, token])
    return jsonify("Menu item updated")

@app.delete('/api/menu')
def menu_delete():
    data = request.json
    # token = request.json('token')
    email = data.get('email')
    restaurant_id =data.get('restaurant_id')
    name = data.get('name')
    id = data.get('id')

    # if token == None:
    #     return jsonify("error,missing token"),400
    if  email  == None:
        return jsonify("menu item does not exist")
    
    result = run_query("SELECT menu_item.id, email,menu_item.name FROM  menu_item INNER JOIN restaurant ON restaurant.id = menu_item.restaurant_id WHERE menu_item.id=? ", [id])
    if result == id :
        run_query("DELETE FROM menu_item WHERE name=?", [name])
        return jsonify('item deleted'),200





    # result = run_query("SELECT restaurant_id , token,id FROM menu INNER JOIN restaurant_session ON restaurant_session.restaurant_id = menu.id WHERE email =? and token = ? ", [email,token])


