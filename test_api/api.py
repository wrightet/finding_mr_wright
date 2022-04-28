from flask import flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    pass



class Locations(Resource):
    pass

api.add_resource(Locations, "/locations")
api.add_resource(Users, '/users')

if __name__ =="__main__":
    app.run()