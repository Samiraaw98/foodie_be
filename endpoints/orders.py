
from app import app 
from helpers.db_helpers import run_query
from flask import  request,jsonify
from flask_cors import CORS
import sys



@app.get('/api/orders')
def order_get():
    order_list = run_query("SELECT * from orders")
    menu_list = run_query("SELECT id from menu_item")
    resp = []
    for order in order_list:
        mn_obj = {}
        mn_obj['id'] = order[0]
        mn_obj['created_at'] = order[1]
        mn_obj['is_confirmed'] = order[2]
        mn_obj['is_completed'] = order[3]
        mn_obj['is_cancelled'] = order[4]
        mn_obj['client_id'] = order[5]
        mn_obj['restaurant_id'] = order[6]
        resp.append(mn_obj)
    for menu in menu_list:
        mn_obj={}
        mn_obj['items'] = menu[0]
        resp.append(mn_obj)

        
    return jsonify(resp) , 200

@app.post('/api/orders')
def order_post():
    data = request.json
    restaurant_id = data.get('restaurant_id')
    id = data.get ('items')


    if not restaurant_id:
        return jsonify('missing restaurant_id'),401
    if not id:
        return jsonify('Missing items'),401


    run_query("INSERT into orders (restaurant_id,items) VALUES (?,?)",[restaurant_id,id])
    return jsonify("Order added"),201



    # if not created_at :
    #     return jsonify("Missing required argument : created_at") , 422
    # if not is_confirmed :
    #     return jsonify ("Missing required argument : is confirmed") , 422
    # if not is_completed:
    #     return jsonify ("Missing required argument : is_completed")
    # if not is_cancelled:
    #     ("Missing required argument: is cancelled ") , 422
    # run_query("INSERT INTO orders (created_at, is_confirmed, is_completed,is_cancelled) VALUES (?,?,?,?)", [created_at,is_confirmed, is_completed, is_cancelled ])
    # return jsonify("order added"), 201

