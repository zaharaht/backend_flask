from backend.db import db
from dataclasses import dataclass

@dataclass
class Region(db.Model):
    __tablename__ = "regions"
    
    name:str
  
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255),unique=True)
    created_by  = db.Column(db.Integer,db.ForeignKey('users.id'))
    created_at = db.Column(db.String(255),nullable=True)
    updated_at = db.Column(db.String(255),nullable=True)
    districts = db.relationship("District",backref="region")
   

    def __init__(self,name,created_by,created_at,updated_at):
     self.name = name
     self.created_by = created_by
     self.created_at = created_at
     self.updated_at = updated_at
    

    def __repr__(self):
        return f"<Region {self.name} >"
  

        
   #save a new instance
    def save(self):
         db.session.add(self)
         db.session.commit()

   #delete the item
    def delete(self):
         db.session.delete(self)
         db.session.commit()