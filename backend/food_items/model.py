from backend.db import db
from dataclasses import dataclass

@dataclass
class FoodItem(db.Model):
  __tablename__ = 'food_items'
  id:int
  name:str
  price:int
  price_unit:str
  image:str
  stock:int
  sub_food_category_id:int

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100),unique=True)
  price = db.Column(db.String(255))  
  price_unit = db.Column(db.String(10),default='UGX')
  image = db.Column(db.String(200))
  stock = db.Column(db.Integer)
  sub_food_category_id = db.Column(db.Integer,db.ForeignKey('sub_food_categories.id'))
  created_by  = db.Column(db.Integer,db.ForeignKey('users.id'))
  created_at = db.Column(db.String(255),nullable=True)
  updated_at = db.Column(db.String(255),nullable=True)
  
