from flask import Flask, render_template, url_for ,request, redirect
import re
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kem'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kemidea/mysite/static/static/ideas.sql'
#db = SQLAlchemy(app)

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
    conn=sqlite3.connect('home/kemidea/mysite/static/ideas.sql')
    cursor=conn.cursor()
    cursor.execute("SELECT idea FROM IDEAS")
    ideas_list=cursor.fetchone()
    cursor.execute("SELECT COUNT(idea) FROM IDEAS")
    idea_count=cursor.fetchone()
    conn.close()
    cursor.close()

    if request.method == "POST":
        idea = request.form["POMYSL"]
        if idea=="" or check_if_exist(idea, ideas_list) or regex_empty.match(idea) or idea.casefold()=="pasierb chuj"or regex.match(idea):
            return redirect(url_for("error"))
        else:
            connn=sqlite3.connect('home/kemidea/mysite/static/ideas.sql')
            cursorn=connn.cursor()
            cursorn.execute("INSERT INTO IDEAS(idea) VALUES (" + idea + ")")
            connn.close()
            cursorn.close()
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
