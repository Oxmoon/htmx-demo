from flask import Flask, flash, jsonify, redirect, render_template, request

app = Flask(__name__)

app.secret_key = "secret"


@app.route("/")
def index():
    return redirect("/todo")


@app.route("/todo")
def todo():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
