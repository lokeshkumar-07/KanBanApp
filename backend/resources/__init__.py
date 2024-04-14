from flask_restful import Api
from .users import User
from .cards import Card
from .lists import List

api = Api(prefix='/api')
api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(List, '/lists', '/lists/<int:id>')
api.add_resource(Card, '/cards/<int:listId>', '/cards/<int:listId>/<int:id>')