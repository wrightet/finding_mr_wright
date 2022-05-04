from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import bcrypt

users_path = "./users.csv"


app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return {'data': data},200
    
    def post(self):
        #password = ''
        #salt = bcrypt.gensalt()
        #hashed = bcrypt.hashpw(password.encode('utf8'), salt)

api.add_resource(Users, "/users")

if __name__ == "__main__":
    app.run(debug=True)