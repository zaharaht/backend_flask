from backend import create_app,db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
 
from backend.users.model import User
from backend.regions.model import Region
from backend.districts.model import District
from backend.addresses.model import Address
from backend.food_categories.model import FoodCategory
from backend.sub_food_categories.model import SubFoodCategory
from backend.food_items.model import FoodItem
from backend.orders.model import Order
# from backend.deliveries.model import Delivery
# from backend.feedbacks.model import Feedback






app = create_app('development')
migrate = Migrate(app,db)
jwt=JWTManager(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,District=District,  Region=Region, User=User,Address=Address,FoodCategory= FoodCategory , FoodItem=FoodItem, Order=Order,SubFoodCategory=SubFoodCategory )  
