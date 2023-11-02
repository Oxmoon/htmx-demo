import os

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import select
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


@app.route("/todos", methods=["GET", "POST"])
def todo():
    todos = Todo.query.all()
    form = CreateTodo()
    if form.validate_on_submit():
        todo = Todo(content=form.todo.data)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html", form=form, todos=todos)


class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)


class CreateTodo(FlaskForm):
    todo = StringField("Todo", validators=[InputRequired(), Length(min=1, max=100)])


if __name__ == "__main__":
    app.run()
