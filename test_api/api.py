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
    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')
        
        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])
            
            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            return {
            'message': f"'{args['userId']}' user not found."
            }, 404
        
class Locations(Resource):
    def get(self):
        data = pd.read_csv(locations_path)
        data = data.to_dict()
        return {'data': data},200

api.add_resource(Locations, "/locations")
api.add_resource(Users, "/users")

if __name__ == "__main__":
    app.run(debug=True)