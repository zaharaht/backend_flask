from flask import  jsonify, request, Blueprint
from backend.addresses.model import Address
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

addresses = Blueprint('addresses', __name__, url_prefix='/addresses')

#get all addresses
@addresses.route("/")
def all_addresses():
    addresses= Address.query.all()
    return jsonify({
            "success":True,
            "data":addresses,
            "total":len(addresses)
        }),200



#creating addresses

@addresses.route('/create', methods= ['POST'])
@jwt_required()
def create_new_address():

    data = request.get_json()
    name = data['name']
    district_id = data['district_id']
    user_id =get_jwt_identity()
    
      
  
    #validations
    if not name:
         return jsonify({'error':"Address name is required"})
   
    if not district_id:
         return jsonify({'error':"District  name is required"})
       #check for an address with same name
    if Address.query.filter_by(name=name).first():
       return jsonify({'error':"This address already exists"})
 

    new_address =Address(name=name,district_id=district_id,user_id=user_id, created_at=datetime.now(),updated_at=datetime.utcnow()) 
      
    #inserting values
    db.session.add( new_address)
    db.session.commit()
    return jsonify({'message':'New address created sucessfully','data':[new_address.id,new_address.name, new_address.district_id, new_address.user_id, new_address.created_at, new_address.updated_at] }),201
          
   
  
    

#get,edit and delete address by id

@addresses.route('/address/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_address(id):
    address = Address.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "id":address.id,
            "name": address.name,
            "district_id": address.district_id,
            "created_at": address.created_at
          
        }
        return {"success": True, "address": response,"message":"Address details retrieved"}

    elif request.method == 'PUT':
        data = request.get_json()

        if not data['name']:
            return jsonify({"message":"address name is required"})
        
        if not data['district_id']:
            return jsonify({"message":"address region name is required"})
        
        
        address.name = data['name']
        address.district_id = data['district_id']
        address.user_id = get_jwt_identity()
        address.updated_at = datetime.utcnow()
        db.session.add(address)
        db.session.commit()
        return {"message": f"{address.name}  address updated successfully"}

    elif request.method == 'DELETE':
        db.session.delete(address)
        db.session.commit()
        return {"message": f"{address.name} address successfully deleted."} 