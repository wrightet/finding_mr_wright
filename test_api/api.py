from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

users_path = "./users.csv"
locations_path = "./locations.csv"

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return {'data': data},200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('city', required=True, type=str)
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
                    'name' :args['name'],
                    'city' :args['city'],
                }, ignore_index=True
            )
            data.to_csv(users_path, index=False)
            return {'data': data.to_dict()}, 200

class Locations(Resource):
    def get(self):
        data = pd.read_csv(locations_path)
        data = data.to_dict()
        return {'data': data},200

api.add_resource(Locations, "/locations")
api.add_resource(Users, "/users")

if __name__ == "__main__":
    app.run(debug=True)