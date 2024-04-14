from flask_restful import Resource, reqparse, abort, Api, fields, marshal_with
from werkzeug.exceptions import InternalServerError, NotFound, HTTPException
from models import Lists as list_model, db, Cards as card_model
from sqlalchemy.exc import SQLAlchemyError
from flask_security import auth_required
from flask_login import current_user
from datetime import date

list_req_data = reqparse.RequestParser()
list_req_data.add_argument('name', required=True, help="list name required")
list_req_data.add_argument('description')



list_field = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'user_id': fields.String,
    'created_date': fields.String,
    'review': fields.String
}

class List(Resource):


    method_decorators = {
        'get': [marshal_with(list_field), auth_required('token')],
        'post': [marshal_with(list_field), auth_required('token')],
        'put': [marshal_with(list_field), auth_required('token')],
        'delete': [auth_required('token')]
    }

    def post(self, id=None):
       
        try:
            data = list_req_data.parse_args()
            if not id:
                list = list_model.query.filter_by(name=data.name, user_id = current_user.id).first()
                if list:
                    raise abort(409, message="List Already exists")
                creted_date = str(date.today())
                list = list_model(**data, created_date = creted_date, user_id = current_user.id)
            else:
                abort(400, message="id not required")
            try:
                db.session.add(list)
                db.session.commit()
                return "data added"
            except SQLAlchemyError:
                db.session.rollback()
                raise InternalServerError('Data could not be added')
        except HTTPException as error:
            raise error
        except BaseException:
            raise InternalServerError("Something Went wrong")

    def get(self, id=None):
        
        try:
            if id:
                try:
                    data = list_model.query.filter_by(id = id, user_id = current_user.id).first()
                except SQLAlchemyError:
                    raise InternalServerError("Could not get the data")
                if not data:
                    raise NotFound("Data Not Found")
            else:
                try:
                    data = list_model.query.filter_by(user_id = current_user.id).all()
                except SQLAlchemyError:
                    raise InternalServerError("coud not fetch the data")
            return data
        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError("Something went wrong")

    def put(self, id=None):
        
        try:
            if not id:
                abort(400, message="id required")
            else:
                try:
                    list = list_model.query.filter_by(id=id, user_id = current_user.id)
                except SQLAlchemyError:
                    raise InternalServerError("could not fetch the data")
                if not list.first():
                    raise NotFound("Data not found")
                else:
                    try:
                        list.update(
                           list_req_data.parse_args())
                        db.session.commit()
                    except SQLAlchemyError:
                        raise InternalServerError("Could not update the data")
                return "data Updated", 200
        except HTTPException as error:
            raise error

        except BaseException:
            raise InternalServerError("Something Went wrong")

    def delete(self, id=None):
       
        try:
            if not id:
                abort(400, message="id required")
            else:
                data = list_model.query.filter_by(id=id, user_id = current_user.id).first()
                # logData = list_model.query.filter_by(user_id = current_user.id, tracker_name = data.tracker_name).all()
                if not data:
                    raise NotFound("data not found")
                else:
                    try:
                        db.session.delete(data)
                        db.session.commit()
                        return "data deleted", 200
                    except SQLAlchemyError:
                        raise InternalServerError("Cound not delete the data")
        except HTTPException as err:
            raise err
        except BaseException:
            raise InternalServerError("Something went wrong")