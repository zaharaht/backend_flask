from backend.db import db
from dataclasses import dataclass

@dataclass
# creating an instance of a class
class SubFoodCategory(db.Model):
    __tablename__="sub_food_categories"

    id:int
    name:str
    food_category_id:int
    


    id=db.Column(db.Integer, primary_key= True)
    name=db.Column(db.String(50), unique= True)
    created_by=db.Column(db.Integer,db.ForeignKey('users.id'))
    created_at=db.Column(db.String(255))
    updated_at=db.Column(db.String(255))
    food_category_id = db.Column(db.Integer,db.ForeignKey('food_categories.id'))
    
    

# defining a function
def __init__(self,name,created_by,created_at,updated_at,food_category_id):
    self.name=name
    self.created_by=created_by
    self.created_at=created_at
    self.updated_at=updated_at
    self.food_category_id=food_category_id


# function representation
def __repr__(self):
        return f"<SubFoodCategory {self.name} >"