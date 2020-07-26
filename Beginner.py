from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail

with open('config.json', 'r') as c:
    params = json.load(c)["parametes"]

app = Flask(__name__)

app.config.update(

    
    MAIL_SERVER=('smtp.gmail.com'),
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USE_TSL=True,
    MAIL_USERNAME='username',
    MAIL_PASSWORD='password'
)

mail = Mail(app)

local_server = "True"

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["productio_uri"]

db = SQLAlchemy(app)


class contactinfo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(20), unique=True, nullable=False)
    Subject = db.Column(db.String(120), unique=False, nullable=False)
    Message = db.Column(db.String(120), unique=False, nullable=False)


class aboutinfo(db.Model):
    srNo = db.Column(db.Integer, primary_key=True)
    EMAIL = db.Column(db.String(30), unique=True, nullable=False)
    Password = db.Column(db.String(30), unique=True, nullable=False)


@app.route("/")
def home():
    return render_template("index.html", params=params)





@app.route("/about", methods=['GET', 'POST'])
def about():
    if (request.method == 'POST'):
        EMAIl = request.form.get('email')
        PASSWORD = request.form.get('pass')
        entry = aboutinfo(EMAIL=EMAIl, Password=PASSWORD)
        db.session.add(entry)
        db.session.commit()


    return render_template("about.html", params=params,About=About)

@app.route("/services")
def service():
          
           return render_template("services.html",params=params,About=About)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = contactinfo(Name=name, Email=email, Subject=subject, Message=message)
        db.session.add(entry)
        db.session.commit()

        mail.send_message(email)

    return render_template("contact.html", params=params)


app.run(debug=True)
