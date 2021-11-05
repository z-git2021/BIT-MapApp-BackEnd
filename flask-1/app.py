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

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    author_id = db.Column(db.Integer,db.ForeignKey("author.id"))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    articles = db.relationship("Article")


@app.route('/t', methods=['GET', 'POST'])
def index5():
    author1 = Author(name="name1")
    article1 = Article(title="p1")
    article2 = Article(title="p2")
    db.session.add(author1)
    db.session.add(article1)
    db.session.add(article1)
    author1.articles.append(article1)
    author1.articles.append(article2)
    db.session.commit()
    article = Article.query.all()
    for i in article:
        print([i.title])
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
            return "post\n"+notes[-1].user+"\n"
        except:
            return "0"

@app.route('/search', methods=["post"])
def index4():
    if request.method == 'POST':
        myform = json.loads(request.data)
        #print(Note.query.filter(Note.user == myform["user"]).all())
        if(Note.query.filter(Note.nickname == myform["nickname"]).all() != []):
            return "1"
    return "0"
@app.route('/login', methods=['POST'])
def index3():
    if request.method == 'POST':
        myform = json.loads(request.data)
        #print(Note.query.filter(Note.user == myform["user"]).all())
        if(Note.query.filter(Note.user == myform["user"]).all() != []):
            userif = Note.query.filter(Note.user == myform["user"])[0]
            if(userif.password == myform["password"]):
                return "1"
    return "0"
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
    app.run()



