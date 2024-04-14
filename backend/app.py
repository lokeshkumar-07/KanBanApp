from flask import Flask, make_response, render_template, jsonify, json
from models import db, User, Lists, Cards
from flask_cors import CORS
from flask_login import current_user
from config import LocalDevelopmentConfig
from resources import api
from utils.security import security, user_datastore
import workers
from mail import send_email
from jinja2 import Template
import tasks
import os
import uuid
import csv
from weasyprint import HTML
from io import StringIO
from datetime import date


celery = None
cors = None


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    api.init_app(app)
    cors = CORS(app)
    security.init_app(app, user_datastore )

    app.app_context().push()


    celery = workers.celery

    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask

    app.app_context().push()

    return app, celery, cors, api



app,celery, cors, api = create_app()

@app.before_first_request
def create_db():
    db.create_all()



@app.route('/api/userdata/<username>')
def user_view(username):
    with open('./templates/pdf.html', 'r') as f:
        template = Template(f.read())

    send_email('lokesh@mail.com', 'welcome', template.render(user= username))
    return username

@app.route('/task_mail/<username>')
def task_mail(username):
    job = tasks.send_welcome_mail("Flaskapp@mail.com", 'Create Task', username)

    return str(job)



@app.route("/api/<user_id>/export")
def pdf_template(user_id):

    user = User.query.filter_by(id = user_id).first()
    email = user.email
    username = user.username
    lists = Lists.query.filter_by(user_id = user.id).all()
    cards = Cards.query.filter_by(user_id = user.id).all()

    # with open('./templates/report.html', 'r') as f:
    #     template = Template(f.read())
    
    message = render_template('report.html', name=username, lists=lists, cards=cards, email=email )

    # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    html = HTML(string=message).write_pdf()

    # file_name = str(username) + '.pdf'
    response = make_response(html)
    # print(file_name)
    # pdf = html.write_pdf(target=file_name)

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Output.pdf'
    
    return response

@app.route("/api/users/<email>")
def user_id(email):

    user = User.query.filter_by(email = email).first()

    return user.id

@app.route("/api/<user_id>/listcsv")
def csv_list(user_id):

    user = User.query.filter_by(id=user_id).first()
    lists = Lists.query.filter_by(user_id = user.id).all()

    data = [{'Id': row.id, 'List Name': row.name, 'List Description': row.description, 'User ID': row.user_id } for row in lists ]

    si = StringIO()
    csv_writer = csv.DictWriter(si, fieldnames=['Id', 'List Name','List Description','User ID'])
    csv_writer.writeheader()
    csv_writer.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/api/<list_id>/cardscsv")
def csv_cards(list_id):

    cards = Cards.query.filter_by(list_id = list_id).all()


    new_cards = []

    for row in cards:
        if row.mark == "Not Complected":
            datenow = str(date.today())
            if datenow > row.deadline:
                temp_list = {'title': row.title, 'content':row.content, 'status': 'Expired'}
            else: 
                temp_list = {'title': row.title, 'content':row.content, 'status': 'Pending' }
        else:
            temp_list = {'title': row.title, 'content':row.content,  'status': row.mark}

        new_cards.append(temp_list)
    
    
    
    data = [{'card title' : row['title'], 'content': row['content'], 'card staus' : row['status']} for row in new_cards]

    si = StringIO()
    csv_writer = csv.DictWriter(si, fieldnames=['card title', 'content', 'card staus', ])
    csv_writer.writeheader()
    csv_writer.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


    

@app.route('/')
def home():
    return "hello"

if "__main__" == __name__:
    app.run(debug=True) 
