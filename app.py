import os
from datetime import datetime

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
    page = int(request.args.get("page", 1))
    if search is not None and search != "":
        todos_set = Todo.query.filter(Todo.content.like("%" + search + "%")).all()
        if request.headers.get("HX-Trigger") == "search":
            return render_template(
                "index.html", todos=todos_set, has_next=False, page=page
            )
    else:
        todos_set = Todo.query.paginate(page=page, per_page=10)

    return render_template(
        "index.html",
        todos=todos_set,
        page=page,
        has_next=todos_set.has_next,
    )
colors = ["lightblue", "turquoise", "#4a71d0", "white"]
@app.route("/todos/colors", methods=["GET"])
def colors_switch():
    cur_col = colors.pop(0)
    colors.append(cur_col)
    return '<h1 id="colChange" hx-get="/todos/colors" hx-swap="outerHTML" class="smooth" hx-trigger="every 1s" style="color:' + cur_col + '">\n'+ 'TODO HTMX App\n'+ '</h1>\n'

@app.route("/todos/count", methods=["GET"])
def todos_count():
    count = Todo.query.count()
    return "(" + str(count) + " total TODOs)"


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

@app.route("/todosLoad/new", methods=["GET"])
def todo_new_get2():
    return redirect("/todos/new")


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


@app.route("/todos/<todo_id>", methods=["DELETE"])
def todos_delete(todo_id=0):
    todo = Todo.query.filter_by(id=todo_id).first_or_404()
    if todo is not None:
        db.session.delete(todo)
        db.session.commit()
    if request.headers.get("HX-Trigger") == "delete-btn":
        flash("Deleted TODO!")
        return redirect(url_for("index"), 303)
    return ""


@app.route("/todos", methods=["DELETE"])
def todos_delete_all():
    todo_ids = list(map(int, request.form.getlist("selected_todo_ids")))
    for todo_id in todo_ids:
        todo = Todo.query.filter_by(id=todo_id).first_or_404()
        db.session.delete(todo)
    db.session.commit()
    flash("Deleted TODOs!")
    todos_set = Todo.query.paginate(page=1, per_page=10)
    return render_template(
        "index.html", todos=todos_set, page=1, has_next=todos_set.has_next
    )


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    due = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(
        db.String, index=True, default=datetime.utcnow().strftime("%Y.%m.%d, %H:%M")
    )


class CreateTodo(FlaskForm):
    todo = StringField("Todo", validators=[InputRequired(), Length(min=1, max=100)])
    due = StringField("Due", validators=[InputRequired(), Length(min=1, max=100)])


class EditTodo(FlaskForm):
    todo = StringField("Todo", validators=[InputRequired(), Length(min=1, max=100)])
    due = StringField("Due", validators=[InputRequired(), Length(min=1, max=100)])


if __name__ == "__main__":
    app.run()
