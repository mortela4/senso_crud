import os
import uuid
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
# from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "sensors_database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

"""
class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Alias: {}>".format(self.title)
"""


class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    alias = db.Column(db.String(50), unique=True)
    type_name = db.Column(db.String(5), unique=False)

    def __init__(self, name=None, alias=None, type_name=None):
        self.name = name
        self.type_name = type_name
        self.alias = alias
        self.id = uuid.uuid4()
        # Debug:
        print("Created sensor: id=%s, alias=%s, type=%s, device=%s" % (self.id, self.alias, self.type_name, self.type_name))

    def __repr__(self):
        return '<ID %r><Name %r><Alias %r><Type %r>' % (self.id, self.name, self.alias, self.type_name)


@app.route('/', methods=["GET", "POST"])
def home():
    sensors = None
    if request.form:
        try:
            sensor = Sensor(title=request.form.get("alias"))
            db.session.add(sensor)
            db.session.commit()
        except Exception as e:
            print("Failed to add sensor!")
            print(e)
    sensors = Sensor.query.all()
    return render_template("home.html", sensors=sensors)


@app.route("/update", methods=["POST"])
def update():
    try:
        newalias = request.form.get("newalias")
        oldalias = request.form.get("oldalias")
        sensor = Sensor.query.filter_by(alias=oldalias).first()
        sensor.alias = newalias
        db.session.commit()
    except Exception as e:
        print("Couldn't update sensor!")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    alias = request.form.get("alias")
    sensor = Sensor.query.filter_by(alias=alias).first()
    db.session.delete(sensor)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)
