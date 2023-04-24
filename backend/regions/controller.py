# Register a new region
from flask import jsonify, request, Blueprint


from backend.regions.model import Region
from backend.db import db
from flask_jwt_extended import get_jwt_identity

from flask_jwt_extended import jwt_required
from datetime import datetime


# Creating a blue print for regions, where regions is the resource
regions = Blueprint('regions',__name__,url_prefix='/regions')

#Getting all regions
@regions.route("/")
def all_regions():
    regions = Region.query.all()
    return jsonify({
            "success":True,
            "data":regions,
            "total":len(regions)
        }),200
 

@regions.route('/create', methods= ['POST'])
@jwt_required()
def create_new_regions():

 
    name =request.json['name']
    created_by = get_jwt_identity()
   
    
      
  
    #validations
    if not name:
         return jsonify({'error':"Region name is required"})
    
    # if not created_by:
    #      return jsonify({'error':"User name is required"})
    

    if Region.query.filter_by(name=name).first():
         return jsonify({'Error': "Region name exists"}), 409 

    new_region = Region(name=name,created_by=created_by,created_at=datetime.now(),updated_at=datetime.utcnow()) 
      
    #inserting values
    db.session.add( new_region)
    db.session.commit()
    return jsonify({'message':'New region created sucessfully','data':[  new_region.name, new_region.created_by,new_region.created_at,new_region.updated_at] }),201
       
@regions.route('/get/<id>', methods=['GET'])
def get_region(id):
    region_id= Region.query.get(id)
    results = {
        "name": region_id.name,
        "created_by": region_id.created_by,
        "created_at": region_id.created_at
        
        
    }   
    return jsonify({"Success": True, "Region": results,"Message":"Region details retrieved"})

          
    # put
@regions.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    region = Region.query.get_or_404(id)

    region.name =request.json['name']
    region.updated_at =datetime.utcnow() 

    db.session.add(region)
    db.session.commit()
    return jsonify({"message":"Region updated successfully"})


# delete
@regions.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    delete_id = Region.query.get(id)

    if delete_id is None:
        return{"Message":"Region doesnot exist"}
    # user doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Region deleted successfully."})
