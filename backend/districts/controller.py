# Register a new district
from flask import jsonify, request, Blueprint
from backend.districts.model import District
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for districts, where districts is the resource
districts = Blueprint('districts',__name__,url_prefix='/districts')

#Getting all districts
@districts.route("/")
def get_all_districts():
    districts = District.query.all()
    return jsonify({
            "success":True,
            "data":districts,
            "total":len(districts)
        }),200

#creating districts


@districts.route('/create', methods= ['POST'])
@jwt_required()
def create_new_district():

    data = request.get_json()
    name = data['name']
    region_id = data['region_id']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
         return jsonify({'error':"District name is required"})
   
    if not region_id:
         return jsonify({'error':"District region name is required"})
    

    if District.query.filter_by(name=name).first() is not None:
        return jsonify({'error': "District name exists"}), 409 

    new_district = District(name=name,region_id=region_id,created_by=created_by,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add( new_district)
    db.session.commit()
    return jsonify({'message':'New district created sucessfully','data': [new_district.id,new_district.name,new_district.region_id,new_district.created_by,new_district.created_at,new_district.updated_at]}),201

@districts.route('/get/<id>', methods=['GET'])
def get_district(id):
    district_id= District.query.get(id)
    results = {
        "name": district_id.name,
        "region_id":district_id.region_id,
        "created_by":district_id.created_by,
        "created_at":district_id.created_at
        
    }
         
    return jsonify({"Success": True, "District": results,"Message":"District details retrieved"})

          
    # put
@districts.route('/update/<int:id>', methods=['PUT'])
def update_district(id):
    district = District.query.get_or_404(id)

    district.name =request.json['name']
    district.region_id =request.json['region_id']
    district.updated_at=datetime.utcnow() 

    db.session.add(district)
    db.session.commit()
    return jsonify({"message":"District updated successfully"})


# delete
@districts.route('/delete/<id>', methods=['DELETE'])
def delete_district(id):
    delete_id = District.query.get(id)

    if delete_id is None:
        return{"Message":"District doesnot exist"}
    # user doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"District deleted successfully."})
