# import dependencies 
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import flask
from flask import Flask , jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Flask Routes
@app.route("/")
def welcome():
    return (f"welcome page <br/>"
           
           f" routes <br/>"
           
           f"/api/v1.0/precipitation <br/>"
           
           f"/api/v1.0/stations <br/>"
           
           f"/api/v1.0/tobs <br/>"

           f"/api/v1.0/start/end<br/>"

          )

# Stations Route           
@app.route("/api/v1.0/stations")

def station():
    result = session.query(Station.station).all()
    st_list = list(np.ravel(result))
    return jsonify (st_list)


#Monthly Temperature Route
@app.route("/api/v1.0/tobs")

def tobs():
    tobss = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2016,8,23').all()
    tobs_list = list(np.ravel(tobss))
    return jsonify (tobs_list)

#Statistic Route
@app.route ("/api/v1.0/<start>/<end>")

def temps(start,end):
    findings = session.query(Measurement).filter(Measurement.date>= start).filter(Measurement.date<=end)
    found =[] 
    for row in findings:
        found.append(row.tobs) 
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))
           
if __name__ == "__main__":
   app.run(debug=True)