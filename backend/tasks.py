from workers import celery
from mail import send_email
from jinja2 import Template
from celery.schedules import crontab
from models import db, User, Lists, Cards
from datetime import date
from flask import render_template

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
   
    sender.add_periodic_task(crontab(0, 0, day_of_month='1'), send_report.s(), name='every 1 month')

   
    sender.add_periodic_task(crontab(minute=0, hour='18'), daily_reminder.s(), name='every day 6 pm' )


#Monthly Report
@celery.task()
def send_report():
    users = User.query.all()

    for i in users:
        with open('./templates/report.html', 'r') as f:
            template = Template(f.read())
        
        user = User.query.filter_by(id = i.id).first()
        email = user.email
        username = user.username
        lists = Lists.query.filter_by(user_id = user.id).all()
        cards = Cards.query.filter_by(user_id = user.id).all()
        
        send_email(i.email, "Your Montly report", template.render(user = username, lists = lists, cards= cards, email = email) )


#daily Reminders
@celery.task()
def daily_reminder():
    users = User.query.all()

    for i in users:
        pending_tasks = []
        cards = Cards.query.filter_by(user_id = i.id).all()
        for j in cards:
            if j.mark == "Not Complected":
                date1 = str(date.today())
                if j.deadline == date1:
                    print(j.deadline, date1)
                    pending_tasks.append(j)
    
        
        
        if len(pending_tasks) != 0 :
            with open('./templates/reminder.html', 'r') as f:
                template = Template(f.read())
            send_email(i.email, "Pending tasks", template.render(cards = pending_tasks, email = i.email))
            
            
@celery.task()
def send_welcome_mail(receiver_mail, sub, username):
    with open('./templates/pdf.html', 'r') as f:
        template = Template(f.read())

    send_email(receiver_mail, sub, template.render(user= username))
    return 'mail sent'