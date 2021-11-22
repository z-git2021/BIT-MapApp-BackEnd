import os
import sys
import json

from flask import Flask,request
from flask import redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired



# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text,unique=True)
    password = db.Column(db.Text)
    nickname = db.Column(db.Text)
    #body = db.Column(db.Text)
    bigarts = db.relationship("Bigart", backref="note")
    smallarts = db.relationship("Smallart", backref="note")

class Smallart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    big_id = db.Column(db.Integer,db.ForeignKey("bigart.id"))
    #bigarts = db.relationship("Bigart", backref="smallart")
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"))
    #notes = db.relationship("Note", backref="note1")

class Bigart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text, unique=True)
    picture = db.Column(db.Text)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))
    #notes = db.relationship("Note", backref="note")
    smallarts = db.relationship("Smallart",backref = "bigart")


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    where = db.Column(db.Text, unique=True)
    bigarts = db.relationship("Bigart", backref="place")



@app.route('/t', methods=['GET', 'POST'])
def index5():
    pic = open('t.png' ,'rb')
    place1 = Place(where = "beihu")
    author1 = Bigart(user="name1")
    article1 = Smallart(title="p1")
    article2 = Smallart(title="p2")
    note1 = Note(user="derby", password="123456",
                nickname="nick")
    db.session.add(place1)
    db.session.add(note1)
    db.session.add(author1)
    db.session.add(article1)
    db.session.add(article2)
    place1.bigarts.append(author1)
    note1.bigarts.append(author1)
    note1.smallarts.append(article1)
    author1.smallarts.append(article1)
    author1.smallarts.append(article2)
    db.session.commit()
    '''author00 = Smallart.query.all()
    for i in author00:
        print([i.title])'''
    print(article1.bigart)
    print(author1.smallarts)
    print(note1)
    print(note1.bigarts)
    print(note1.smallarts[0].note)
    print(note1.bigarts[0].smallarts[0].bigart.note)
    print(place1.bigarts[0].smallarts)
    return "print all"

@app.route('/', methods=['GET', 'POST'])
def index():
    notes = Note.query.all()
    #print(Note.query.filter(Note.user == "flying derby")[0])
    for i in notes:
        print([i.user,i.password,i.nickname])
    return "print all"
@app.route('/register', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        #print(request.form.get("user"))
        myform = json.loads(request.data)
        note = Note(user = myform["user"],password = myform["password"],nickname = myform["nickname"])
        try:
            db.session.add(note)
            db.session.commit()
            notes = Note.query.all()
            js = {"result":"success","user": notes[-1].user}
            myfiles = json.dumps(js)
            return myfiles+"\n"
        except:
            js = {"result": "fail"}
            myfiles = json.dumps(js)
            return myfiles + "\n"

@app.route('/search', methods=["post"])
def index4():
    if request.method == 'POST':
        myform = json.loads(request.data)
        #print(Note.query.filter(Note.user == myform["user"]).all())
        if(Note.query.filter(Note.nickname == myform["user"]).all() != []):
            js = {"result": "success", "nickname": Note.query.filter(Note.nickname == myform["nickname"]).all()[0].user}
            myfiles = json.dumps(js)
            return myfiles + "\n"
    js = {"result": "fail"}
    myfiles = json.dumps(js)
    return myfiles + "\n"
@app.route('/login', methods=['POST'])
def index3():
    if request.method == 'POST':
        print(request.data)
        print(json.loads(request.data))
        myform = json.loads(request.data)
        #print(Note.query.filter(Note.user == myform["user"]).all())
        if(Note.query.filter(Note.user == myform["user"]).all() != []):
            userif = Note.query.filter(Note.user == myform["user"])[0]
            if(userif.password == myform["password"]):
                js = {"result": "success"}
                myfiles = json.dumps(js)
                return myfiles + "\n"
    js = {"result": "success"}
    myfiles = json.dumps(js)
    return myfiles + "\n"
@app.route('/clear', methods=['GET', 'POST'])
def index1():
    notes = Note.query.all()
    while(len(notes)>0):
        db.session.delete(notes[0])
        db.session.commit()
        notes = Note.query.all()
    print(notes)
    return "0"



if __name__ == '__main__':
    print("?")
    db.drop_all()
    db.create_all()
    note = Note(user="flying derby", password="123456",
                nickname="nick")
    db.session.add(note)
    db.session.commit()
    app.run(debug=False, host='192.168.43.204', port=5000)



