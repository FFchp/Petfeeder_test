#flask
import re
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
# create Flask
app = Flask(__name__)

# create conn database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# create conn api
api = Api(app)

# design model database
class Usermodel(db.Model):
    __tablename__ = 'user'
    no = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

class information_(db.Model):
    __tablename__ = 'information'
    no = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String(100))
    info = db.Column(db.Text)
    time = db.Column(db.DateTime)
    def __repr__(self):
        return f"information(no = {information_.no}, topic = {information_.topic}, info = {information_.info}, time = {information_.time})"

class food_brand(db.Model):
    __tablename__ = 'food_brand'
    no = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    age = db.Column(db.String(20))
    Favor = db.Column(db.String(50))
    info = db.Column(db.Text)
    time = db.Column(db.DateTime)

class info_for_RerDer(db.Model):
    __tablename__ = 'rerder'
    no = db.Column(db.Integer, primary_key = True)
    weight = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    meal = db.Column(db.Integer)
    status = db.Column(db.String(50))

class calories(db.Model):
    __tablename__ = 'calorie'
    no = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime)
    vol = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('Usermodel.no'))

class waters(db.Model):
    __tablename__ = 'waters'
    no = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime)
    vol = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('Usermodel.no'))

class record_rerder(db.Model):
    __tablename__ = 'record_rerder'
    no = db.Column(db.Integer, primary_key = True)
    rer = db.Column(db.Integer)
    der = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    eat = db.Column(db.Integer)
    rerder_id = db.Column(db.Integer)
    mem_id = db.Column(db.Integer)

db.create_all()

# Request Parser
user_add_args = reqparse.RequestParser()
user_add_args.add_argument('username', type = str, required = True, help='???????????????????????? Username')
user_add_args.add_argument('password', type = str, required = True, help='???????????????????????? Password')
user_add_args.add_argument('email', type = str, required = True, help='???????????????????????? Email')

# login
login_add_args = reqparse.RequestParser()
login_add_args.add_argument('username', type = str, required = True, help='???????????????????????? Username')
login_add_args.add_argument('password', type = str, required = True, help='???????????????????????? Password')

information_add_args = reqparse.RequestParser()
information_add_args.add_argument('weight', type = int, required = True, help = '???????????????????????? weight')
information_add_args.add_argument('month', type = int, required = True, help = '???????????????????????? month')
information_add_args.add_argument('year', type = int, required = True, help = '???????????????????????? year')
information_add_args.add_argument('meal', type = int, required = True, help = '???????????????????????? meal')
information_add_args.add_argument('status', type = str, required = True, help = '???????????????????????? status')

Resource_field_usermodel = {
    'no' : fields.Integer,
    'username' : fields.String,
    'password' : fields.String,
    'email' : fields.String
}

Resource_field_rerder = {
    'no' : fields.Integer,
    'wieght' : fields.Integer,
    'month' : fields.Integer,
    'year' : fields.Integer,
    'meal' : fields.Integer,
    'status' : fields.String
}

Resource_field_calorie = {
    'no' : fields.Integer,
    'time' : fields.DateTime(dt_format='rfc822'),
    'cal' : fields.Integer,
    'user_id' : fields.Integer
}

Resource_field_water = {
    'no' : fields.Integer,
    'timestamp' : fields.DateTime(dt_format='rfc822'),
    'vol' : fields.Integer,
    'user_id' : fields.Integer
}

Resource_field_rerder = {
    'no' : fields.Integer,
    'weight' : fields.Integer,
    'month' : fields.Integer,
    'year' : fields.Integer,
    'meal': fields.Integer,
    'status' : fields.String
}

class Home(Resource):
    def get(self):
        return {'msg':'Hello Flask API'}

class rerDer(Resource):
    #@marshal_with(Resource_field_rerder)
    def get(self, no):
        result = info_for_RerDer.query.filter_by(no = no).order_by(info_for_RerDer.no.desc()).first()
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
                result_ = record_rerder(rer = rer, der = derN, eat = eat, rerder_id = no, mem_id = no)
                show = {"rer" : rer, "der" : derN, "eat" : eat, "rerder_id" : no, "mem_id" : no}
                #return show, 200

            elif (result.status == 'obese') : # Der obese
                derN = 1.4 * rer
                print("You choose OBESE PRONE")    
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                #result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
                result_ = record_rerder(rer = rer, der = derN, eat = eat, rerder_id = no, mem_id = no)
                show = {"rer" : rer, "der" : derN, "eat" : eat, "rerder_id" : no, "mem_id" : no}
                #return show, 200

            elif (result.status == 'weight loss') : # Der weight loss
                derN = 1.0 * rer
                print("You choose WEIGHT LOSS")
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                #result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
                result_ = record_rerder(rer = rer, der = derN, eat = eat, rerder_id = no, mem_id = no)
                show = {"rer" : rer, "der" : derN, "eat" : eat, "rerder_id" : no, "mem_id" : no}
                #return show, 200

            elif (result.status == 'normal') : # Der Normal
                derN = 2 * rer
                print("You choose SET NORMAL")
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                #result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}    
                result_ = record_rerder(rer = rer, der = derN, eat = eat, rerder_id = no, mem_id = no)
                show = {"rer" : rer, "der" : derN, "eat" : eat, "rerder_id" : no, "mem_id" : no}
                #return show, 200

        db.session.add(result_)
        db.session.commit()
        return show, 200

class add_weight(Resource):
    def post(self):
        args = information_add_args.parse_args()
        argsdb = info_for_RerDer(weight = args['weight'], month = args['month'], year = args['year'], meal = args['meal'], status = args['status'])
        #argsdb = info_for_RerDer(weight = weight, month = month, year = year, meal = meal, status = status)
        info = {"weight" : argsdb.weight, "month" : argsdb.month, "year" : argsdb.year, "meal" : argsdb.meal, "status" : argsdb.status}
        db.session.add(argsdb)
        db.session.commit()
        return info, 201

class add_user(Resource):
    @marshal_with(Resource_field_usermodel)
    #def post(self, username, password, email):
    def post(self):
        args = user_add_args.parse_args()
        argsdb = Usermodel(username = args['username'], password = args['password'], email = args['email'])
        result = Usermodel.query.filter_by(username = args['username']).first()
        if result:
            abort(409, message = 'Username ?????????')
        else:
            #user = Usermodel(username = username, password = password, email = email)
            db.session.add(argsdb)
            db.session.commit()
            return argsdb, 201

class information(Resource):
    def get(Resource, topic):
        result = information_.query.filter_by(topic = topic).first()
        result_ = {"topic" : result.topic, "information": result.info}
        print(type(result))
        print(result_)
        return result_

class get_user(Resource):
    def post(self):
        args = login_add_args.parse_args()
        password = args['password']
        result = Usermodel.query.filter_by(username = args['username']).first()
        print(result)
        print(type(result))
        if not result:
            abort(404, message = 'Wrong Username or Password')
        else:
            if  result.password == password:
                print(password, ' ', result.password)
                msg = {"msg" : "correct"}
                return msg, 200
            else:
                abort(400, message = 'Wrong Username or Password')

class brand(Resource):
    def get(self, name):
        result = food_brand.query.filter_by(name = name).first()
        if not result:
            abort(404, message = '?????????????????????????????????????????????????????????????????????')
        else:
            result_ = {"name" : name, "age" : result.age, "favor" : result.Favor, "info" : result.info}
        return result_

class info_rerder(Resource):
    @marshal_with(Resource_field_rerder)
    def get(self):
        result = info_for_RerDer.query.order_by(info_for_RerDer.no).all()
        print(result)
        print(type(result))
        return result, 200

class User(Resource):
    @marshal_with(Resource_field_usermodel)
    def get(self):
        result = Usermodel.query.order_by(Usermodel.no).all()
        print(result)
        print(type(result))
        return result, 200

class byid_rerder(Resource):
    @marshal_with(Resource_field_rerder)
    def get(self, id):
        result = info_for_RerDer.query.filter_by(no = id).all()
        print(result)
        print(type(result))
        return result, 200

'''
class add_img(Resource):
    #@marshal_with()
    def post(self, id):
        pass
    def update():
        pass
'''

class cal(Resource):
    @marshal_with(Resource_field_calorie)
    def get(self):
        result = calories.query.order_by(calories.no).all()
        print(result)
        print(type(result))
        return result, 200

class water(Resource):
    @marshal_with(Resource_field_water)
    def get(self):
        result = waters.query.order_by(waters.no).all()
        print(result)
        print(type(result))
        return result, 200

# Call
api.add_resource(Home, '/')                           # home ??????????????????
api.add_resource(User, '/user')                       # get all user
#api.add_resource(add_user, '/add_user/<string:username>/<string:password>/<string:email>')   # register
api.add_resource(add_user, '/add_user')               # Register ??????????????????
api.add_resource(get_user, '/login')                  #log in ??????????????????
api.add_resource(information, '/info/<string:topic>') # information
api.add_resource(brand, '/brand/<string:name>')       # show brand ??????????????????
api.add_resource(rerDer, '/rerder/<int:no>')          # rerDer ??????????????????
api.add_resource(add_weight, '/add')                  #add weight ??????????????????
api.add_resource(info_rerder, '/get_rerder')           # get all rer, der value
api.add_resource(byid_rerder, '/byid_rerder/<int:id>') # get all rer, der by id 
api.add_resource(cal, '/calories')                     # get cal  
api.add_resource(water, '/water')                      # get water ??????????????????


# run debug
if __name__ == '__main__':
    app.run(debug = True, host ='0.0.0.0')
