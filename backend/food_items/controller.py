# Register a new order
from flask import jsonify, request, Blueprint
from backend.food_items.model import FoodItem
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for orders, where orders is the resource
food_items = Blueprint('food_items',__name__,url_prefix='/food_items')

#Getting all orders
@food_items.route("/")
def get_all_fooditems():
    food_items = FoodItem.query.all()
    return jsonify({
            "success":True,
            "data":food_items,
            "total":len(food_items)
        }),200

#creating districts


@food_items.route('/create', methods= ['POST'])
@jwt_required()
def create_new_fooditems():

    data = request.get_json()
    name = data['name']
    price = data['price']
    price_unit = data['price_unit']
    image = data['image']
    stock = data['stock']
    sub_food_category_id = data['sub_food_category_id']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
        return jsonify({'error':"Food item name is required"})
   
    if not price:
        return jsonify({'error':"Food item cost is required"})
    
    if not price_unit:
        return jsonify({'error':"The cost of food item perunit is required"})

    if not image:
        return jsonify({'error':" Food item image is required"})
    
    if not stock:
        return jsonify({'error':"The amount food item in stock  is required"})
    if not sub_food_category_id:
        return jsonify({'error':" Sub Food category name  is required"})
         
    

    if FoodItem.query.filter_by(name=name).first() is not None and FoodItem.query.filter_by(created_by=created_by).first():
        return jsonify({'error': "This food item  already exsists"}), 409 

    food_item = FoodItem(name=name,created_by=created_by,price=price,price_unit=price_unit,image=image,stock=stock,sub_food_category_id=sub_food_category_id,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add( food_item)
    db.session.commit()
    return jsonify({'message':'New food item created sucessfully','data': [food_item.id,food_item.name,food_item.created_by,food_item.price,food_item.created_at,food_item.updated_at,food_item.price_unit,food_item.image,food_item.stock, food_item.sub_food_category_id]}),201

@food_items.route('/get/<id>', methods=['GET'])
def get_fooditem(id):
    food_item_id= FoodItem.query.get(id)
    results = {
        "id":food_item_id.id,
        "name": food_item_id.name,
        "price":food_item_id.price,
        "price_unit":food_item_id.price_unit,
        "image":food_item_id.image,
        "stock":food_item_id.stock,
        "sub_food_category_id":food_item_id.sub_food_category_id,
        "created_by":food_item_id.created_by,
        "created_at":food_item_id.created_at
        
    }
    
    return jsonify({"Success": True, "FoodItem": results,"Message":"Food item details retrieved"})

          
    # put
@food_items.route('/update/<id>', methods=['PUT'])
def update_fooditem(id):
    food_item = FoodItem.query.get_or_404(id)

    food_item.name =request.json['name']
    food_item.price =request.json['price']
    food_item.price_unit =request.json['price_unit']
    food_item.image =request.json['image']
    food_item.stock =request.json['stock']
    food_item.sub_food_category_id =request.json['sub_food_category_id']
    food_item.updated_at=datetime.utcnow() 

    db.session.add(food_item)
    db.session.commit()
    return jsonify({"message":"Food item updated successfully"})


# delete
@food_items.route('/delete/<id>', methods=['DELETE'])
def delete_fooditem(id):
    delete_id = FoodItem.query.get(id)

    if delete_id is None:
        return{"Message":"Food item doesnot exist"}
    # user doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Food item deleted successfully."})
        
   
  
  