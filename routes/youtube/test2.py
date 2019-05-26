from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

class TodoList(Resource):
    def get(self):
        return "TODOS"
    def test(self):
        return "cesur"