from flask_security import Security, SQLAlchemyUserDatastore
from models import db
from models import User, Role
import flask_security.core as fc



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = fc.Security()