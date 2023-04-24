# Register a new subfoodcategory
from flask import jsonify, request, Blueprint
from backend.sub_food_categories.model import SubFoodCategory
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for subfoodcategory, where subfoodcategory is the resource
sub_food_categories = Blueprint('sub_food_categories',__name__,url_prefix='/sub_food_categories')

#Getting all sub_food_categories
@sub_food_categories.route("/")
def get_all_subfoodcategories():
    sub_food_categories = SubFoodCategory.query.all()
    return jsonify({
            "success":True,
            "data":sub_food_categories,
            "total":len(sub_food_categories)
        }),200

#creating subfoodcategory


@sub_food_categories.route('/create', methods= ['POST'])
@jwt_required()
def create_new_subfoodcategory():

    data = request.get_json()
    name = data['name']
    food_category_id = data['food_category_id']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
         return jsonify({'error':"Sub food category name is required"})
   
    if not food_category_id:
         return jsonify({'error':"The food category name is required"})
    

    if SubFoodCategory.query.filter_by(name=name).first() is not None:
        return jsonify({'error': "Sub food category name exists"}), 409 

    new_sub_food_category = SubFoodCategory(name=name,food_category_id=food_category_id,created_by=created_by,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add(new_sub_food_category)
    db.session.commit()
    return jsonify({'message':'New Sub food category created sucessfully','data': [new_sub_food_category.id,new_sub_food_category.name,new_sub_food_category.food_category_id,new_sub_food_category.created_by,new_sub_food_category.created_at,new_sub_food_category.updated_at]}),201

@sub_food_categories.route('/get/<id>', methods=['GET'])
def get_subfoodcategory(id):
    sub_food_category_id= SubFoodCategory.query.get(id)
    results = {
        "name": sub_food_category_id.name,
        "food_category_id":sub_food_category_id.food_category_id,
        "created_by":sub_food_category_id.created_by,
        "created_at":sub_food_category_id.created_at
        
    }
         
    return jsonify({"Success": True, "SubFoodCategory": results,"Message":"Sub food category details retrieved"})

          
    # put
@sub_food_categories.route('/update/<int:id>', methods=['PUT'])
def update_subfoodcategory(id):
    sub_food_category = SubFoodCategory.query.get_or_404(id)

    sub_food_category.name =request.json['name']
    sub_food_category.food_category_id =request.json['food_category_id']
    sub_food_category.updated_at=datetime.utcnow() 

    db.session.add(sub_food_category)
    db.session.commit()
    return jsonify({"message":"Sub food category updated successfully"})


# delete
@sub_food_categories.route('/delete/<id>', methods=['DELETE'])
def delete_subfoodcategory(id):
    delete_id = SubFoodCategory.query.get(id)

    if delete_id is None:
        return{"Message":"Sub food category doesnot exist"}
    # subfoodcategory doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Sub food category deleted successfully."})
