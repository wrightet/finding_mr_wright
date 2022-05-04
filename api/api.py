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
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('first', required=True)
        parser.add_argument('last', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('birth', required=True)
        parser.add_argument(self.encode('password'), required=True)
        args = parser.parse_args()
        data = pd.read_csv(users_path)
        if args['userId'] in data['userId']:
            return {
                'message': f"{args['userId']} already exists"
            }
        else:
            data = data.append(
                {
                    'userId' :args['userId'],
                    'first' :args['first'],
                    'last' :args['last'],
                    'email' :args['email'],
                    'birth' :args['birth'],
                    'password' :args['password']
                }, ignore_index=True
            )
            data.to_csv(users_path, index=False)
            return {'data': data.to_dict()}, 200

    def encode(password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf8'), salt)

api.add_resource(Users, "/users")

if __name__ == "__main__":
    app.run(debug=True)