from flask import Flask

app = Flask(__name__)


from endpoints import client , client_session, restaurant, restaurant_session, menu,orders

