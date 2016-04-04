import sys
import random
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

BASECOORDS = [-13.9626, 33.7741]

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude_off = db.Column(db.Float)
    longitude_off = db.Column(db.Float)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    district = db.relationship("District")

    def __init__(self, id, district, lat, lng):
        self.id = id
        self.district = district
        self.latitude_off = lat
        self.longitude_off = lng

    def __repr__(self):
        return "<Point %d: Lat %s Lng %s>" % (self.id, self.latitude_off, self.longitude_off)

    @property
    def latitude(self):
        return self.latitude_off + self.district.latitude

    @property
    def longitude(self):
        return self.longitude_off + self.district.longitude


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, id, name, lat, lng):
        self.id = id
        self.name = name
        self.latitude = lat
        self.longitude = lng


@app.route('/')
def index():
    districts = District.query.all()
    return render_template('index.html', districts=districts)


@app.route('/district/<int:district_id>')
def district(district_id):
    points = Point.query.filter_by(district_id=district_id).all()
    coords = [[point.latitude, point.longitude] for point in points]
    return jsonify({"data": coords})


def make_random_data(db):
    NDISTRICTS = 5
    NPOINTS = 10
    for did in range(NDISTRICTS):
        district = District(did, "District %d" % did, BASECOORDS[0], BASECOORDS[1])
        db.session.add(district)
        for pid in range(NPOINTS):
            lat = random.random() - 0.5
            lng = random.random() - 0.5
            row = Point(pid + NPOINTS * did, district, lat, lng)
            db.session.add(row)
    db.session.commit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'mkdb':
            db.create_all()
            make_random_data(db)
    else:
        app.run(debug=True)
