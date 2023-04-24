# Register a new subfoodcategory
from flask import jsonify, request, Blueprint
from backend.food_categories.model import FoodCategory
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for subfoodcategory, where subfoodcategory is the resource
food_categories = Blueprint('food_categories',__name__,url_prefix='/food_categories')

#Getting all sub_food_categories
@food_categories.route("/")
def get_all_foodcategories():
    food_categories = FoodCategory.query.all()
    return jsonify({
            "success":True,
            "data":food_categories,
            "total":len(food_categories)
        }),200

#creating subfoodcategory


@food_categories.route('/create', methods= ['POST'])
@jwt_required()
def create_new_foodcategory():

    data = request.get_json()
    name = data['name']
    image = data['image']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
         return jsonify({'error':"Food category name is required"})
    
    # if not image:
    #      return jsonify({'error':"Food category name is required"})

    if FoodCategory.query.filter_by(name=name).first() is not None:
        return jsonify({'error': "Food category name exists"}), 409 

    new_food_category = FoodCategory(name=name,image=image,created_by=created_by,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add(new_food_category)
    db.session.commit()
    return jsonify({'message':'New Food category created sucessfully','data': [new_food_category.id,new_food_category.name,new_food_category.created_by,new_food_category.created_at,new_food_category.updated_at]}),201

@food_categories.route('/get/<id>', methods=['GET'])
def get_foodcategory(id):
    food_category_id= FoodCategory.query.get(id)
    results = {
        "name": food_category_id.name,
        "created_by":food_category_id.created_by,
        "created_at":food_category_id.created_at
        
    }
         
    return jsonify({"Success": True, "FoodCategory": results,"Message":" Food category details retrieved"})

          
    # put
@food_categories.route('/update/<int:id>', methods=['PUT'])
def update_subfoodcategory(id):
    food_category = FoodCategory.query.get_or_404(id)

    food_category.name =request.json['name']
    food_category.updated_at=datetime.utcnow() 

    db.session.add(food_category)
    db.session.commit()
    return jsonify({"message":" Food category updated successfully"})


# delete
@food_categories.route('/delete/<id>', methods=['DELETE'])
def delete_foodcategory(id):
    delete_id = FoodCategory.query.get(id)

    if delete_id is None:
        return{"Message":" Food category doesnot exist"}
    # subfoodcategory doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Food category deleted successfully."})
    
   
  