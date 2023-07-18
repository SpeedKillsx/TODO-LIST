from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
app.app_context().push()
class TODO(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String)
    done = db.Column(db.Boolean)
    def __init__(self, todo, done):
        self.todo = todo
        self.done = done
        


@app.route('/')
def index():
    #!Get all the data from database
    database_data = db.session.execute(db.select(TODO)).scalars()
    #* Create a temporary list to save the data
    temp_data = []
    for v in database_data:
        temp_data.append({"todo":v.todo, "done":v.done})
        #todos.append({"todo":v.todo, "done":v.done})
            #print(todos)
    todos = temp_data
    temp_data = []
    return render_template("index.html", todos=todos)

@app.route("/add", methods = ["POST"])
def add():
    #!Get all the data from database
    #the 'todo' iq the name of the input
    todo = request.form['todo']
    if todo!="":
        #* Add the data to the database
        data_todo = TODO(todo, None)
        db.session.add(data_todo)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods = ["POST", "GET"])
def edit(index):
    #!Get all the data from database
    database_data = db.session.execute(db.select(TODO)).scalars()
    temp_data = []
    for v in database_data:
        temp_data.append({"todo":v.todo, "done":v.done})
        #todos.append({"todo":v.todo, "done":v.done})
            #print(todos)
    todos = temp_data
    temp_data = []
    #! Start Updating
    todo = todos[index]
    todo_temp = todo['todo']
    if request.method == "POST":
        todo['todo'] = request.form['todo']
        query = db.session.query(TODO)
        query = query.filter(TODO.todo == todo_temp)
        query.update(dict(todo=todos[index]['todo'], done=False))
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo = todo, index = index)

@app.route("/check/<int:index>")
def check(index):
    #!Get all the data from database
    database_data = db.session.execute(db.select(TODO)).scalars()
    temp_data = []
    for v in database_data:
        temp_data.append({"todo":v.todo, "done":v.done})
        #todos.append({"todo":v.todo, "done":v.done})
    todos = temp_data
    temp_data = []
    todos[index]['done'] = not todos[index]['done']
    query = db.session.query(TODO)
    query = query.filter(TODO.todo == todos[index]['todo'])
    query.update(dict(todo=todos[index]['todo'], done=True))
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route('/delete/<int:index>')
def delete(index):
    #!Get all the data from database
    database_data = db.session.execute(db.select(TODO)).scalars()
    temp_data = []
    for v in database_data:
        temp_data.append({"todo":v.todo, "done":v.done})
        #todos.append({"todo":v.todo, "done":v.done})
    todos = temp_data
    temp_data = []
    TODO.query.filter(TODO.todo == todos[index]['todo']).delete()
    db.session.commit()
    del todos[index]
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)