#flask
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
    #def __repr__(self):
    #    return f"uesr(username = {username}, password = {password}, email = {email})"

class information_(db.Model):
    __tablename__ = 'information'
    no = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String(100))
    info = db.Column(db.Text)
    time = db.Column(db.DateTime)
    def __repr__(self):
        return f"uesr(no = {information_.no}, topic = {information_.topic}, info = {information_.info}, time = {information_.time})"

class food_brand(db.Model):
    __tablename__ = 'food_brand'
    no = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    age = db.Column(db.String(20))
    Favor = db.Column(db.String(50))
    info = db.Column(db.Text)
    time = db.Column(db.DateTime)

class rerder(db.Model):
    __tablename__ = 'rerder'
    no = db.Column(db.Integer, primary_key = True)
    weight = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    meal = db.Column(db.Integer)
    status = db.Column(db.String(50))

db.create_all()

# Request Parser
user_add_args = reqparse.RequestParser()
user_add_args.add_argument('username', type = str, required = True, help='กรุณาใส่ Username')
user_add_args.add_argument('password', type = str, required = True, help='กรุณาใส่ Password')
user_add_args.add_argument('email', type = str, required = True, help='กรุณาใส่ Email')

information_add_args = reqparse.RequestParser()
information_add_args.add_argument('weight', type = int, required = True, help = 'กรุณาใส่ weight')
information_add_args.add_argument('month', type = int, required = True, help = 'กรุณาใส่ month')
information_add_args.add_argument('year', type = int, required = True, help = 'กรุณาใส่ year')
information_add_args.add_argument('meal', type = int, required = True, help = 'กรุณาใส่ meal')
information_add_args.add_argument('status', type = str, required = True, help = 'กรุณาใส่ status')

Resource_field={
    'no' : fields.Integer,
    'username' : fields.String,
    'password' : fields.String,
    'email' : fields.String
}

class rerDer(Resource):
    def get(self, no):
        result = rerder.query.filter_by(no = no).first()
        #print(result)
        #print(type(result))
        result_ = {"msg" : "404 Error"}
        #print(type(result_))
        
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
                result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
            elif (result.status == 'obese') : # Der obese
                derN = 1.4 * rer
                print("You choose OBESE PRONE")    
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
            elif (result.status == 'weight loss') : # Der weight loss
                derN = 1.0 * rer
                print("You choose WEIGHT LOSS")   
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}
            elif (result.status == 'normal') : # Der Normal
                derN = 2 * rer
                print("You choose SET NORMAL")
                print("DER per day : ", derN , "kcal/day")
                eat = derN / result.meal
                result_ = {"Weight": result.weight, "Month" : result.month, "Year" : result.year, "Status" : result.status, "Rer" : rer, "Der" : derN, "Meals" : result.meal, "CalPerMeal" : eat}    
        return result_

class add_weight(Resource):
    def post(self):
        args = information_add_args.parse_args()
        argsdb = rerder(weight = args['weight'], month = args['month'], year = args['year'], meal = args['meal'], status = args['status'])
        db.session.add(argsdb)
        db.session.commit()
        return args, 201

class Home(Resource):
    def get(self):
        return {'msg':'Hello Flask API'}

class User(Resource):
    @marshal_with(Resource_field)
    def get(self):
        result = Usermodel.query.order_by(Usermodel.no).all()
        print(result)
        print(type(result))
        return result, 200
    def post(self):
        args = user_add_args.parse_args()
        result = Usermodel.query.filter_by(username = args['username']).first()
        if result:
            abort(409, message = 'Username ซ้ำ')
        user = Usermodel(username = args['username'], password = args['password'], email = args['email'])
        db.session.add(user)
        db.session.commit()
        return args, 201

class information(Resource):
    def get(Resource, topic):
        result = information_.query.filter_by(topic = topic).first()
        result_ = {"topic" : result.topic, "information": result.info}
        print(type(result))
        print(result_)
        return result_

class get_user(Resource):
    def get(self, username):
        result = Usermodel.query.filter_by(username = username).first()
        print(result)
        print(type(result))
        if not result:
            abort(404, message = 'ไม่พบ username ที่ร้องขอ')
        else:
            result_ = {"username" : username, "password" : result.password, "email" : result.email}
        return result_, 200

class brand(Resource):
    def get(self, name):
        result = food_brand.query.filter_by(name = name).first()
        if not result:
            abort(404, message = 'ไม่พบชนิดอาหารที่ร้องขอ')
        else:
            result_ = {"name" : name, "age" : result.age, "favor" : result.Favor, "info" : result.info}
        return result_

# call
api.add_resource(Home, '/')
api.add_resource(User, '/user')
api.add_resource(get_user, '/get_user/<string:username>')
api.add_resource(information, '/info/<string:topic>')
api.add_resource(brand, '/brand/<string:name>')
api.add_resource(rerDer, '/rerder/<int:no>')
api.add_resource(add_weight, '/add')

# run debug
if __name__ == '__main__':
    app.run(debug = True)
