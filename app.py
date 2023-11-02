import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return redirect("/todos")


@app.route("/todos", methods=["GET"])
def todo():
    search = request.args.get("q")
    if search is not None:
        todos_set = Todo.query.filter(Todo.content.like("%" + search + "%")).all()
    else:
        todos_set = Todo.query.all()
    return render_template("index.html", todos=todos_set)


@app.route("/todos/<todo_id>", methods=["GET"])
def todos_view(todo_id=0):
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    return render_template("show.html", todo=todo)


@app.route("/todos/<todo_id>/edit", methods=["GET"])
def todos_edit_get(todo_id=0):
    form = EditTodo()
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    return render_template("edit.html", todo=todo, form=form)


@app.route("/todos/<todo_id>/edit", methods=["POST"])
def todos_edit_post(todo_id=0):
    form = EditTodo()
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    if form.validate_on_submit():
        todo.content = form.todo.data
        todo.due = form.due.data
        db.session.commit()
        flash("Edited TODO!")
        return redirect(url_for("todos_view", todo_id=todo.id))
    else:
        return render_template("edit.html", todo=todo, form=form)


@app.route("/todos/new", methods=["GET"])
def todo_new_get():
    form = CreateTodo()
    return render_template("new.html", form=form)


@app.route("/todos/new", methods=["POST"])
def todo_new():
    form = CreateTodo()
    if form.validate_on_submit():
        todo = Todo(content=form.todo.data, due=form.due.data)
        db.session.add(todo)
        db.session.commit()
        flash("Created new TODO!")
        return redirect(url_for("index"))
    return render_template("new.html", form=form)


@app.route("/todos/<todo_id>/delete", methods=["POST"])
def todos_delete(todo_id=0):
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    if todo is not None:
        db.session.delete(todo)
        db.session.commit()
        flash("Deleted TODO!")
    return redirect(url_for("index"))


class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    due = db.Column(db.String(100), nullable=False)


class CreateTodo(FlaskForm):
    todo = StringField("Todo", validators=[InputRequired(), Length(min=1, max=100)])
    due = StringField("Due", validators=[InputRequired(), Length(min=1, max=100)])


class EditTodo(FlaskForm):
    todo = StringField("Todo", validators=[InputRequired(), Length(min=1, max=100)])
    due = StringField("Due", validators=[InputRequired(), Length(min=1, max=100)])


if __name__ == "__main__":
    app.run()
