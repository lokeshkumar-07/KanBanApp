from flask_restful import Resource, marshal_with, reqparse, fields, abort
from flask_security import auth_required
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, HTTPException, NotFound
from models import db, Cards as card_model, Lists as list_model
import datetime
from datetime import date

card_req_data = reqparse.RequestParser()
card_req_data.add_argument('title', required=True, help="Title is required")
card_req_data.add_argument('content')
card_req_data.add_argument('deadline')
card_req_data.add_argument('mark'),
card_req_data.add_argument('complete_date')


card_fields = {
    'id' : fields.Integer,
    'list_id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'deadline': fields.String,
    'mark': fields.String,
    'complete_date': fields.String
}

class Card(Resource):
    method_decorators = {
        'get': [marshal_with(card_fields), auth_required('token')],
        'post': [marshal_with(card_fields), auth_required('token')],
        'put' : [marshal_with(card_fields), auth_required('token')],
        'delete': [auth_required('token')]
    }

    def post(self, listId=None, id=None):
        try:
            if id:
                abort(400, 'id not required')
            else:
                data = card_req_data.parse_args()
            try:
                
                card = card_model(**data,list_id=listId, user_id = current_user.id)
                list = list_model.query.filter_by(id = listId).first()
                current_date_time = datetime.datetime.now()
                formatted_date_time = current_date_time.strftime("%d %B %Y %I:%M %p")
                list.review = formatted_date_time
                db.session.add(card)
                db.session.commit()
            except SQLAlchemyError:
                raise InternalServerError('card could not be added')
            
            return data

        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError('Somthing went wrong')

    def get(self, listId=None, id=None):
        try:
            if id:
                try: 
                    data = card_model.query.filter_by(list_id=listId, user_id = current_user.id, id  = id).first()
                except SQLAlchemyError:
                    raise InternalServerError('Could not fetch card from database')
                if not data:
                    raise NotFound('data not found')
            else :
                try:
                    data = card_model.query.filter_by(list_id=listId, user_id = current_user.id).all()
                except SQLAlchemyError:
                    raise InternalServerError('could not fetch cards from database!')
                if not data :
                    raise NotFound('data not found')

            return data
        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError('Something went wrong')

    def put(self, listId=None, id=None):
        try:
            if not id:
                abort(404, 'id required')
            else:
                try:
                    log = card_model.query.filter_by(id=id, user_id = current_user.id)
                except SQLAlchemyError:
                    raise InternalServerError('could not fetch card from database')
                if not log.first():
                    abort(404, 'data not found')
                else:
                    try:
                        data = card_req_data.parse_args()
                        log.update(data)
                        list = list_model.query.filter_by(id= listId).first()
                        current_date_time = datetime.datetime.now()
                        formatted_date_time = current_date_time.strftime("%d %B %Y %I:%M %p")
                        list.review = formatted_date_time
                        db.session.commit()
                    except SQLAlchemyError:
                        raise InternalServerError('Could not update card in database')
        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError('Something went wrong!')
        
    def delete(self, listId=None, id= None):
        try:
            if not id: 
                abort(404, 'id required')
            else:
                try:
                    card = card_model.query.filter_by(id=id,list_id=listId, user_id = current_user.id).first()
                except SQLAlchemyError:
                    raise InternalServerError('Count not fetch card from database')
                if not card:
                    abort(404,message='data not found')
                else:
                    try:
                        data = db.session.delete(card)
                        db.session.commit()
                        return data
                    except SQLAlchemyError:
                        raise InternalServerError('count not delete card in database')
        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError('Something went wrong!')