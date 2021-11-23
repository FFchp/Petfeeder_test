#flask
import re
from flask import Flask
from flask.scaffold import _matching_loader_thinks_module_is_package
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

from main import Resource_field_rerder
# create Flask
app = Flask(__name__)

# create conn database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/PetfeederV3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# create conn api
api = Api(app)

# match table in database
class user(db.Model):
    __tablename__ = 'user'
    MEM_ID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

class information(db.Model):
    __tablename__ = 'information'
    No = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String(100))
    info = db.Column(db.Text)
    time = db.Column(db.DateTime)
    def __repr__(self):
        return f"information(no = {information.no}, topic = {information.topic}, info = {information.info}, time = {information.time})"

class food_brand(db.Model):
    __tablename__ = 'food_brand'
    No = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    age = db.Column(db.String(20))
    favor = db.Column(db.String(50))
    info = db.Column(db.Text)
    time = db.Column(db.DateTime)

class water(db.Model):
    __tablename__ = 'water'
    wt_no = db.Column(db.Integer, primary_key = True)
    wt_time = db.Column(db.DateTime)
    wt_quantity = db.Column(db.Integer)
    MEM_ID = db.Column(db.Integer, primary_key = True)

class Status(db.Model):
    __tablename__ = 'Status'
    NO = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.Integer)
    Time = db.Column(db.DateTime)

class cal_rerder(db.Model):
    __tablename__ = 'cal_rerder'
    No = db.Column(db.Integer, primary_key = True)
    rer = db.Column(db.Integer)
    der = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    rerder_id = db.Column(db.Integer, db.ForeignKey('rerder.rerder_id'))

class rerder(db.Model):
    __tablename__ = 'rerder'
    rerder_id = db.Column(db.Integer, primary_key = True)
    dog_name = db.Column(db.String(50))
    weight = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    meal = db.Column(db.Integer)
    status = db.Column(db.String(50))
    MEM_ID = db.Column(db.Integer, db.ForeignKey('user.MEM_ID'))

class food(db.Model):
    __tablename__ = 'food'
    No = db.Column(db.Integer, primary_key = True)
    Food = db.Column(db.Integer)
    Time = db.Column(db.DateTime)
    MEM_ID = db.Column(db.Integer, db.ForeignKey('user.MEM_ID'))

class calorie(db.Model):
    __tablename__ = 'calorie'
    No = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime)
    vol = db.Column(db.Integer)
    MEM_ID = db.Column(db.Integer, db.ForeignKey('user.MEM_ID'))

db.create_all() # create all table

# resource field
Resource_field_usermodel = {
    'no' : fields.Integer,
    'username' : fields.String,
    'password' : fields.String,
    'email' : fields.String
}

Resource_field_rerder ={
    'rerder_id' : fields.Integer,
    'dog_name' : fields.String,
    'weight' : fields.Integer,
    'month' : fields.Integer,
    'year' : fields.Integer,
    'meal' : fields.Integer,
    'status' : fields.String,
    'MEM_ID' : fields.Integer
}

Resource_field_brand = {
    'No' : fields.Integer,
    'name' : fields.String,
    'age' : fields.String,
    'favor' : fields.String,
    'info' : fields.String,
    'time' : fields.DateTime,
}

Resource_field_water = {
    'wt_no' : fields.Integer,
    'wt_time' : fields.DateTime(dt_format='rfc822'),
    'wt_quantity' : fields.Integer,
    'MEM_ID' : fields.Integer
}
Resource_field_info = {
    'No' : fields.Integer,
    'topic' : fields.String,
    'info' : fields.String,
    'time' : fields.DateTime(dt_format='rfc822')
}

# Request Parser
#register
user_add_args = reqparse.RequestParser()
user_add_args.add_argument('username', type = str, required = True, help='กรุณาใส่ Username')
user_add_args.add_argument('password', type = str, required = True, help='กรุณาใส่ Password')
user_add_args.add_argument('email', type = str, required = True, help='กรุณาใส่ Email')

# login
login_add_args = reqparse.RequestParser()
login_add_args.add_argument('username', type = str, required = True, help='กรุณาใส่ Username')
login_add_args.add_argument('password', type = str, required = True, help='กรุณาใส่ Password')

# weight
weight_add_args = reqparse.RequestParser()
weight_add_args.add_argument('dog_name', type = str, required = True, help = 'กรุณาใส่ dog_name')
weight_add_args.add_argument('weight', type = int, required = True, help = 'กรุณาใส่ weight')
weight_add_args.add_argument('month', type = int, required = True, help = 'กรุณาใส่ month')
weight_add_args.add_argument('year', type = int, required = True, help = 'กรุณาใส่ year')
weight_add_args.add_argument('meal', type = int, required = True, help = 'กรุณาใส่ meal')
weight_add_args.add_argument('status', type = str, required = True, help = 'กรุณาใส่ status')
weight_add_args.add_argument('MEM_ID', type = int, required = True, help='กรุณาใส่ MEM_ID')

# brand
brand_add_args = reqparse.RequestParser()
brand_add_args.add_argument('name', type = str, required = True, help = 'กรุณาใส่ brand')

# water
water_add_args = reqparse.RequestParser()
water_add_args.add_argument('wt_no', type = int, required = True, help = 'กรุณาใส่ no')

# infomation
info_add_args = reqparse.RequestParser()
info_add_args.add_argument('topic', type = str, required = True, help = 'ใส่ topic')

# rerder
rerder_add_args = reqparse.RequestParser()
rerder_add_args.add_argument('rerder_id', type = int)
'''
rerder_add_args.add_argument('weight', type = int)
rerder_add_args.add_argument('month', type = int)
rerder_add_args.add_argument('year', type = int)
rerder_add_args.add_argument('meal', type = int)
rerder_add_args.add_argument('status', type = str)
rerder_add_args.add_argument('MEM_ID', type = int)
'''

# Design Api
class Home(Resource):
    def get(self):
        return{'msg' : 'Hello Flask api'}

# Register
class add_user(Resource):
    @marshal_with(Resource_field_usermodel)
    #def post(self, username, password, email):
    def post(self):
        args = user_add_args.parse_args()
        argsdb = user(username = args['username'], password = args['password'], email = args['email'])
        result = user.query.filter_by(username = args['username']).first()
        if result:
            abort(409, message = 'Username ซ้ำ')
        else:
            db.session.add(argsdb)
            db.session.commit()
            return argsdb, 201

# login
class login(Resource):
    def post(self):
        args = login_add_args.parse_args()
        password = args['password']
        print(password)
        result = user.query.filter_by(username = args['username']).first()
        print(result.password)
        if not result:
            abort(404, message = 'Wrong Username or Password')
        else:
            if  result.password == password:
                print(password, ' ', result.password)
                msg = {"msg" : "correct"}
                return msg, 200
            else:
                abort(400, message = 'Wrong Username or Password')

#add weight
class weight(Resource):
    def post(self):
        args = weight_add_args.parse_args()
        argsdb = rerder(dog_name = args['dog_name'] ,weight = args['weight'], month = args['month'], year = args['year'], meal = args['meal'], status = args['status'])
        #result = rerder.query.filter_by(dog_name = args['dog_name']).first()
        #if not result:
        #    abort(400, message = '')
        db.session.add(argsdb)
        db.session.commit()
        return argsdb, 201

# get brand
class brand(Resource):
    @marshal_with(Resource_field_brand)
    def get(self):
        args = brand_add_args.parse_args()
        result = food_brand.query.filter_by(name = args['name']).first()
        if not result:
            abort(404, message = 'ไม่พบอาหารที่ร้องขอ')
        else:
            return result

# water
class waters(Resource):
    @marshal_with(Resource_field_water)
    def get(self):
        result = water.query.order_by(water.wt_no).all()
        print(result)
        print(type(result))
        return result, 200

# water by id
class water_id(Resource):
    @marshal_with(Resource_field_water)
    def get(self):
        args = water_add_args.parse_args()
        result = water.query.filter_by(wt_no = args['wt_no']).all()
        return result, 200

# information
class informations(Resource):
    @marshal_with(Resource_field_info)
    def get(self):
        args = info_add_args.parse_args()
        result = information.query.filter_by(topic = args['topic']).first()
        return result, 200

# calculate rerder
class Calculate(Resource):
    def get(self):
        args = rerder_add_args.parse_args()
        result = rerder.query.filter_by(rerder_id = args['rerder_id']).order_by(rerder.rerder_id.desc()).first()
        eat = result.meal
        #print(result)
        #print(type(result))
        if not result:
            abort(404, message = "Don't found value")
        #print(type(result_))
        #return result
        # Rer Calculate
        rer = 0
        if result.weight >= 12 and result.weight <= 24 : # Send to DB
            rer = (30 * result.weight) + 70
            print("Your dog need " , rer , "kcal per day")
        else : # Send to DB
            rer2 = result.weight ** 0.75
            rer = rer2 * 70
            print("Your dog need " , rer , "kcal per day")

        # Der Calculate
        derN = 0
        if result.year == 0 and result.month <= 4 : # Der
            derN = 3 * rer
            print("DER per day : ", derN , "kcal/day")
        else :
            if (result.status == 'neutered') : # Der Neutered
                derN = 1.6 * rer
                print("You choose NEUTERED") 
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                #result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}
                #return show, 200

            elif (result.status == 'obese') : # Der obese
                derN = 1.4 * rer
                print("You choose OBESE PRONE")    
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                #result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}
                #return show, 200

            elif (result.status == 'weight loss') : # Der weight loss
                derN = 1.0 * rer
                print("You choose WEIGHT LOSS")
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                #result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}
                #return show, 200

            elif (result.status == 'normal') : # Der Normal
                derN = 2 * rer
                print("You choose SET NORMAL")
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                #result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}
                #return show, 200
        # add to database
        db.session.add(result_)
        db.session.commit()
        return show, 200

class get_rerder_byid(Resource):
    args = rerder_add_args.parse_args()
    #result = rer

# Call api
api.add_resource(Home, '/')
api.add_resource(add_user, '/add_user') # register
api.add_resource(login, '/login')       # login
api.add_resource(brand, '/brand')       # food_brand
api.add_resource(waters, '/water')      # query water
api.add_resource(water_id, '/water_id') # get waters id
api.add_resource(informations, '/information') # get information
api.add_resource(Calculate, '/calculate')      # calulate
api.add_resource(weight, '/add_weight')        # add dog personal info


# run_debug
if __name__ == '__main__':
    app.run(debug = True, host ='0.0.0.0')
