from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# existing engine
engine = create_engine('sqlite:///Todo.db')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
#session = Session()
app = Flask(__name__)

engine = create_engine('sqlite:///Todo.db')
Base = declarative_base()


class Todo(Base):
    __tablename__ = 'Todo'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    complete = Column(Boolean)


@app.route("/")
def home():
    session = Session()
    todo_list = session.query(Todo).all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    session = Session()
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    session.add(new_todo)
    session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    session = Session()
    todo = session.query(Todo).filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    session = Session()
    session.query(Todo).filter_by(id=todo_id).delete()
    session.commit()
    return redirect(url_for("home"))

Base.metadata.create_all(engine)
if __name__ == "__main__":

    app.run(debug=True)
