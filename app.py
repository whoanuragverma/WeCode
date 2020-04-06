from flask import Flask, render_template,request,redirect,url_for,jsonify,make_response
from others import randomStringDigits
from flask_sqlalchemy import SQLAlchemy
from time import ctime
from hashlib import md5
import os
import psycopg2 2.8.5


app = Flask(__name__)
app.config['SECRET_KEY'] = "djXEHjRAPPtzjNQRl7eJ.53/mgQDGWktEechrRhP45Ez"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Code(db.Model):
    ms = db.Column('code_id',db.String(6),primary_key = True)
    cd = db.Column(db.String(100000))
    ip = db.Column(db.String(48))
    time = db.Column(db.String(70))

    def __init__(self,ms,cd,ip,time):
        self.ms = ms
        self.cd = cd
        self.ip = ip
        self.time = time

@app.route('/')
def home():
    ID = randomStringDigits() 
    data = Code(ms=ID,cd="",ip="",time="")
    db.session.add(data)
    db.session.commit()
    response = make_response(redirect(url_for('main',word=ID)))
    trial = 1
    while request.cookies.get('ID' + str(trial)) != None:
        trial += 1 
    response.set_cookie('ID' + str(trial) ,md5(ID.encode()).hexdigest(),max_age=60*60*24)
    response.set_cookie('admin','true')
    response.set_cookie('_gwa',ctime())
    return response

@app.route('/<word>')
def main(word):
    trial = 1
    while (request.cookies.get('ID' + str(trial)) != None) or (request.cookies.get('ID' + str(trial)) == md5(word.encode()).hexdigest()):
        if request.cookies.get('admin') == 'true':
            return render_template('show.html',data = Code.query.filter_by(ms=word).first())
        trial += 1
    return render_template('disp.html',ajaxdata=word)


@app.route('/json/<word>')
def jsonresp(word):
    data = Code.query.filter_by(ms=word).first()
    return jsonify({"code":data.cd,"ip":data.ip,"time":data.time})

@app.route('/edit/<word>',methods=['POST'])
def edit(word):
    if request.method == 'POST':
        data = Code.query.filter_by(ms=word).first()
        data.cd = request.form['code']
        data.ip = request.form['ip']
        data.time = request.form['date']
        db.session.commit()
        return jsonify({"response":"saved","time":ctime()})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
