# Register a new order
from flask import jsonify, request, Blueprint
from backend.orders.model import Order
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for orders, where orders is the resource
orders = Blueprint('orders',__name__,url_prefix='/orders')

#Getting all orders
@orders.route("/")
def get_all_orders():
    orders = Order.query.all()
    results =[
        {
        "id":order.id,
        "quantity":order.quantity,
        "status":order.status,
        "address_id":order.address_id,
        "food_item_id":order.food_item_id,
        "created_by":order.created_by,
        "created_at":order.created_at,
        "updated_at":order.updated_at
        } for order in orders
    ]
    return{"count": len(results), "orders": results}

#creating districts


@orders.route('/create', methods= ['POST'])
@jwt_required()
def create_new_order():

    data = request.get_json()
    quantity = data['quantity']
    status = 'Confirmed'
    address_id = data['address_id']
    food_item_id = data['food_item_id']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not quantity:
         return jsonify({'error':"Order quantity is required"})
   
    if not status:
         return jsonify({'error':"Status is required,its either confirmed or pending"})
    
    if not address_id:
         return jsonify({'error':"Address from where the order is made is required"})

    if not food_item_id:
         return jsonify({'error':"Name of food item ordered is required"})
         
    

    if Order.query.filter_by(created_by=created_by).first() is not None and Order.query.filter_by(food_item_id=food_item_id).first():
        return jsonify({'error': "This order has already been made"}), 409 

    new_order = Order(quantity=quantity,created_by=created_by,status=status,address_id=address_id,food_item_id=food_item_id,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add( new_order)
    db.session.commit()
    return jsonify({'message':'New order created sucessfully','data': [new_order.id,new_order.quantity,new_order.status,new_order.created_by,new_order.created_at,new_order.updated_at,new_order.address_id,new_order.food_item_id]}),201

@orders.route('/order/<id>', methods=['GET'])
def get_orders(id):
    order_id= Order.query.get(id)
    results = {
        "quantity": order_id.quantity,
        "status":order_id.status,
        "address_id":order_id.address_id,
        "food_item_id":order_id.food_item_id,
        "created_by":order_id.created_by,
        "created_at":order_id.created_at
        
    }
         
    return jsonify({"Success": True, "Order": results,"Message":"Order details retrieved"})

          
    # put
@orders.route('/update/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)

    order.quantity =request.json['quantity']
    order.status =request.json['status']
    order.address_id =request.json['address_id']
    order.food_item_id =request.json['food_item_id']
    order.updated_at=datetime.utcnow() 

    db.session.add(order)
    db.session.commit()