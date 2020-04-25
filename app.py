from flask import Flask, render_template, url_for ,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import re

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'kem'
#app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:////../static/ideas.sql'

app.config['MYSQL_DATBASE_HOST'] = 'kemidea.mysql.pythonanywhere-services.com'
app.config['MYSQL_DATABASE_USER'] = 'kemidea'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Behaviour2@'
app.config['MYSQL_DATABASE_DB'] = 'kemidea$KEM'
mysql = MySQL(app)



regex = re.compile("p(\s)?a(\s)?s(\s)?i(\s)?e(\s)?r(\s)?b\s+c(\s)?h(\s)?u(\s)?j(\s)?",re.IGNORECASE)
regex_empty = re.compile("/s+")
#class DBModel(db.Model):
#        __tablename__= 'IDEAS'
#        id = db.Column('id', db.Integer, primary_key=True)
#        idea = db.Column('idea', db.Unicode)

#        def __init__ (self,idea):
#                self.idea = idea


#ex = DBModel("witam")

#db.session.add(ex)
#db.session.commit()

def check_if_exist(input, db_list):
    for data in db_list:
        if(data.casefold() == input.casefold()):
            return True
    return False

@app.route('/', methods= ["POST","GET"])
def hello_world():
    curr = mysql.connection.cursor()
    curr.execute("SELECT idea FROM IDEAS")
    mysql.connection.commit()
    ideas_list = curr.fetchall()
    curr.execute("SELECT COUNT(idea) FROM IDEAS")
    mysql.connection.commit()
    idea_count = curr.fetchall()
    curr.close()

#    for ids in db_ideas:
 #       idea_count += 1
 #       ideas_list.append(ids.idea)

    if request.method == "POST":
        idea = request.form["POMYSL"]
        if idea=="" or check_if_exist(idea, ideas_list) or regex_empty.match(idea) or idea.casefold()=="pasierb chuj"or regex.match(idea):
            return redirect(url_for("error"))
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO IDEAS(idea) VALUES (%s)", (idea))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("sql_added"))
    else:
        return render_template("index.html", idea_count=idea_count, ideas_list=ideas_list)

@app.route("/mamciebatonie")
def error():
        return render_template('baton.html')

@app.route("/welldone")
def sql_added():
        return render_template('welldone.html')

if __name__ == '__main__':
    app.run()

