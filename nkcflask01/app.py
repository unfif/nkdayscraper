from flask import Flask, render_template, redirect, request
from model import ToDoList, init_db

app = Flask(__name__)

db = init_db(app)

todolist = ToDoList()

# @app.route("/")
# def show_todolist():
#   return render_template("index.html", todolist=todolist.get_all())

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/additem", methods=["POST"])
def add_item():
  title = request.form["title"]
  if not title:
    return redirect("/")

  todolist.add(title)
  return redirect("/")

@app.route("/deleteitem/<int:item_id>")
def delete_todoitem(item_id):
  todolist.delete(item_id)
  return redirect("/")

@app.route("/deletealldoneitems")
def delete_alldoneitems():
  todolist.delete_doneitem()
  return redirect("/")

@app.route("/updatedone", methods=["POST"])
def update_done():
  keys = request.form.keys()
  items = [int(x) for x in keys]
  todolist.update_done(items)
  return redirect("/")
