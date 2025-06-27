from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tasks = Task.query.filter_by(is_done=False).all()
    tasks_done = Task.query.filter_by(is_done=True).all()
    return render_template("index.html", tasks=tasks, tasks_done=tasks_done)

@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form["task"]
    new_task = Task(description=task_text, is_done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.is_done = True
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
