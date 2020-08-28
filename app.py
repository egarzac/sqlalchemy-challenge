#set FLASK_APP=app
#FLASK run

#Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# 1. import Flask
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
    "Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/2016-08-23<br/>"
    f"/api/v1.0/2016-08-23/2016-08-30<br/>"
)

# 4. Queries
# Route 1: Precipitation
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)
    return jsonify(precipitation)

# Route 2: Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

# Route 3: TOBS
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    session.close()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

# Route 4: Start Date (work in progress)
@app.route("/api/v1.0/2016-08-23")
def start():
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs).label('min'),func.max(Measurement.tobs).label('max'),func.avg(Measurement.tobs).label('avg')).all()
    session.close()
    maxtob = list(np.ravel(results))
    return jsonify(maxtob)

if __name__ == "__main__":
    app.run(debug=True)
