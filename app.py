import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlite3

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def main():
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).\
                order_by(Measurement.date).all()
    result_dict = dict(results)
    return jsonify(result_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.id)).\
            group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()

    stations_list = list(stations)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    max_temp = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= year_ago).all()

    tobs_list = list(max_temp)
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    tobsall = []

    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)
        
    return jsonify(tobsall)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()


    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

if __name__ == '__main__':
    app.run(debug=True)