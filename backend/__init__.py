from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from backend.db import db
#from flask_jwt_extended import JWTManager
from flask_cors import CORS
#from flask_jwt_extended import get_jwt_identity



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config[config_name])
    Config[config_name].init_app(app)
    
    #app.config["JWT_ALGORITHM"] = "HS256"
    app.config.from_pyfile("../config.py")
    app.app_context()
    
  


    db.init_app(app)
    CORS(app)
    
   
    #importing blueprint
   
    from backend.users.controller import users
    from backend.regions.controller import regions
    from backend.districts.controller import districts
    from backend.addresses.controller import addresses
    from backend.food_categories.controller import food_categories
    from backend.sub_food_categories.controller import sub_food_categories
    from backend.food_items.controller import food_items
    from backend.orders.controller import orders
    #from backend.deliveries.controller import deliveries
    #from backend.feedbacks.controller import feedbacks
   
    
   
      #registering blueprint for the route to work
      #app.register_blueprint(users) takes in the blueprint instance as the paramenter.
    
    app.register_blueprint(users)
    app.register_blueprint(regions)
    app.register_blueprint(districts)
    app.register_blueprint(addresses)
    app.register_blueprint(sub_food_categories) 
    app.register_blueprint(food_categories)
    app.register_blueprint(food_items)
    app.register_blueprint(orders)
    # app.register_blueprint(deliveries)
    # app.register_blueprint(feedbacks)
  


    return app