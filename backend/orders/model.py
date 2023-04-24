from backend.db import db
from dataclasses import dataclass


class Order(db.Model):
    __tablename__ = "orders"
    id:int
    quantity:str
    address_id:int
    food_item_id:int

    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.String(255))
    status=db.Column(db.String(255))
    address_id = db.Column(db.Integer,db.ForeignKey('addresses.id'))
    created_by=db.Column(db.Integer,db.ForeignKey('users.id'))
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
    created_at=db.Column(db.String(255))
    updated_at=db.Column(db.String(255))


    def __init__(self, quantity,status,address_id, created_by,food_item_id, created_at,updated_at):
     self.quantity = quantity
     self.status=status
     self.address_id = address_id
     self.created_by = created_by
     self.food_item_id = food_item_id
     self.created_at = created_at
     self.updated_at = updated_at
    

    def __repr__(self):
        return f"<Order {self.user_id} >"