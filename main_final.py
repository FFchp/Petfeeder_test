#flask
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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
    wt_time = db.Column(db.Date)
    wt_quanitity = db.Column(db.Integer)
    MEM_ID = db.Column(db.Integer, primary_key = True)

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
    'MEM_ID' : fields.Integer,
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
    'wt_time' : fields.DateTime(dt_format='iso8601'),
    'wt_quanitity' : fields.Integer,
    'MEM_ID' : fields.Integer
}
Resource_field_info = {
    'No' : fields.Integer,
    'topic' : fields.String,
    'info' : fields.String,
    'time' : fields.DateTime(dt_format='iso8601')
}

Resource_field_calrerder = {
    'no' : fields.Integer,
    'rer' : fields.Integer,
    'der' : fields.Integer,
    'timestamp' : fields.DateTime,
    'rerder_id' : fields.Integer
}

Resource_field_calorie = {
    'no' : fields.Integer,
    'time' : fields.DateTime(dt_format='iso8601'),
    'vol' : fields.Integer,
    'MEM_ID' : fields.Integer
}

Resource_field_food = {
    'No' : fields.Integer,
    'Time' : fields.DateTime(dt_format='iso8601'),
    'Food' : fields.Integer,
    'MEM_ID' : fields.Integer
}

Resource_field_graph_cal = {
    'no' : fields.Integer,
    'time' : fields.DateTime(dt_format='iso8601'),
    'vol' : fields.Integer,
    'MEM_ID' : fields.Integer
}

Resource_field_only_vol = {
    'No' : fields.Integer,
    'vol' : fields.Integer
}

# Request Parser
# register
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

# rerder
no_add_args = reqparse.RequestParser()
no_add_args.add_argument('no', type = int)

# calories
calorie_add_args = reqparse.RequestParser()
calorie_add_args.add_argument('MEM_ID', type = int)

# food
food_add_args = reqparse.RequestParser()
food_add_args.add_argument('MEM_ID', type = int)

# Design Api
class Home(Resource):
    def get(self):
        return{'msg' : 'Hello Flask api'}

# Register
class add_user(Resource):
    @marshal_with(Resource_field_usermodel)
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
        result = user.query.filter_by(username = args['username']).first()
        print(result)
        if not result:
            return {"status" : 1, "msg" : "Your username or Password is Wrong"}
        else:
            if  result.password == password:
                print(password, ' ', result.password)
                msg = {"status" : 0, "id" : result.MEM_ID}
                return msg, 200
            else:
                return {"status" : 1, "msg" : "Your username or Password is Wrong"}

# add weight
class weight(Resource):
    def post(self):
        args = weight_add_args.parse_args()
        argsdb = rerder(dog_name = args['dog_name'] ,weight = args['weight'], month = args['month'], year = args['year'], meal = args['meal'], status = args['status'])
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
        if not result:
            abort(404, message = "Don't found value")
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
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}

            elif (result.status == 'obese') : # Der obese
                derN = 1.4 * rer
                print("You choose OBESE PRONE")    
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}

            elif (result.status == 'weight loss') : # Der weight loss
                derN = 1.0 * rer
                print("You choose WEIGHT LOSS")
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}

            elif (result.status == 'normal') : # Der Normal
                derN = 2 * rer
                print("You choose SET NORMAL")
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                result_ = cal_rerder(rer = rer, der = derN, rerder_id = args['rerder_id'])
                show = {"rer" : rer, "der" : derN, "meal" : eat, "rerder_id" : args['rerder_id']}

        # add to database
        db.session.add(result_)
        db.session.commit()
        return show, 200

class get_rer_byid(Resource):
    @marshal_with(Resource_field_calrerder)
    def get(self):
        args = no_add_args.parse_args()
        result = cal_rerder.query.filter_by(no = args['no']).all()
        return result, 200

class calories(Resource):
    @marshal_with(Resource_field_calorie)
    def get(self):
        args = calorie_add_args.parse_args()
        result = calorie.query.filter_by(MEM_ID = args['MEM_ID']).all()
        return result, 200

class foods(Resource):
    @marshal_with(Resource_field_food)
    def get(self):
        args = food_add_args.parse_args()
        result = food.query.filter_by(MEM_ID = args['MEM_ID']).all()
        return result, 200

class graph_7day(Resource):
    @marshal_with(Resource_field_graph_cal)
    def get(self):
        args = food_add_args.parse_args()
        #SELECT SUM(vol), time from calorie group by DATE(time) ORDER BY time desc limit 5
        result = db.session.query(calorie.vol, calorie.time, calorie.MEM_ID).filter_by(MEM_ID = args['MEM_ID']).group_by(calorie.time).order_by(calorie.time.desc()).all()
        #result = db.session.query(func.sum(calorie.vol), calorie.time, calorie.MEM_ID).filter_by(MEM_ID = args['MEM_ID']).group_by(calorie.time).order_by(calorie.time.desc()).all()
        return result

class graph_7day_water(Resource):
    @marshal_with(Resource_field_water)
    def get(self):
        args = food_add_args.parse_args()
        #result = db.session.query(func.sum(water.wt_quanitity), water.wt_time, water.MEM_ID, water.wt_no).filter_by(MEM_ID = args['MEM_ID']).group_by(water.wt_time).order_by(water.wt_time.desc()).all()
        #result = db.session('SELECT SUM(vol), time from calorie group by DATE(time) ORDER BY time desc limit 5')
        #result = db.session.query(sum(water.WT_QUANTITY), water.WT_TIME, water.MEM_ID, water.WT_NO).filter_by(MEM_ID = args['MEM_ID']).group_by(water.WT_TIME).order_by(water.WT_TIME.desc()).all()
        result = db.session.query(water.wt_quanitity, water.wt_time, water.MEM_ID, water.wt_no).filter_by(MEM_ID = args['MEM_ID']).order_by(water.wt_time.desc()).all()
        return result

class query_all_calorie(Resource):
    @marshal_with(Resource_field_graph_cal)
    def get(self):
        result = calorie.query.order_by(calorie.time).all()
        return result

class query_all_cal(Resource):
    @marshal_with(Resource_field_only_vol)
    def get(self):
        args = food_add_args.parse_args()
        result = db.session.query(calorie.vol, calorie.No).filter_by(MEM_ID = args['MEM_ID']).order_by(calorie.No.desc()).all()
        return result

# Call api
api.add_resource(Home, '/')
api.add_resource(add_user, '/add_user')                     # register
api.add_resource(login, '/login')                           # login
api.add_resource(brand, '/brand')                           # food_brand
api.add_resource(informations, '/information')              # get information
api.add_resource(Calculate, '/calculate')                   # calulate
api.add_resource(weight, '/add_weight')                     # add dog personal info
api.add_resource(get_rer_byid, '/rer_byid')                 # get rer der by id
api.add_resource(calories, '/calories')                     # get cal by id
api.add_resource(foods, '/food')                            # get food by id
api.add_resource(waters, '/water')                          # query all water
api.add_resource(water_id, '/water_id')                     # get waters by id
api.add_resource(graph_7day, '/graph')                      # graph
api.add_resource(query_all_calorie, '/query_all_calorie')   # query all node-red
api.add_resource(graph_7day_water, '/water_graph')          # water_graph
api.add_resource(query_all_cal, '/get_vol')                 # get only volumn

# run_debug
if __name__ == '__main__':
    app.run(debug = True, host ='0.0.0.0')
