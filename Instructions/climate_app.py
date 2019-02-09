import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from datetime import datetime as dt
import datetime

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)






#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all Climate api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement).all()
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict[measurement.date] = measurement.prcp        
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
   
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from the last data point in the database
    max_date = session.query(func.max(Measurement.date)).scalar()
    
    max_dt = dt.strptime(max_date, "%Y-%m-%d")
    max_last_year_dt = datetime.datetime(max_dt.year -1, max_dt.month, max_dt.day).date()
    

    # Perform a query to retrieve the data and precipitation scores
    rows = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= max_last_year_dt).all() 

    all_tobs =[]

    for row in rows:
        tobs={}
        tobs[row.date] = row.tobs
        all_tobs.append(tobs)

    return jsonify(all_tobs)

    
@app.route("/api/v1.0/<start_date>")
def date_range(start_date):
    print(f"Start Date : {start_date}")
    
    results = session.query( func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    all_tobs =[]

    for row in results:
        tobs={}
        tobs["Start_date"] = start_date
        tobs["min_temp"] = row[0]
        tobs["avg_temp"] = row[1]
        tobs["max_temp"] = row[2]
        all_tobs.append(tobs)

    return jsonify(all_tobs)    


@app.route("/api/v1.0/<start_date>/<end_date>")
def date_ranges(start_date, end_date):
    print(f"Start Date : {start_date}")
    print(f"End Date : {end_date}")
    
    results = session.query( func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    all_tobs =[]

    for row in results:
        tobs={}
        tobs["Start_date"] = start_date
        tobs["End_date"] = end_date
        tobs["min_temp"] = row[0]
        tobs["avg_temp"] = row[1]
        tobs["max_temp"] = row[2]
        all_tobs.append(tobs)

    return jsonify(all_tobs)    



if __name__ == '__main__':
    app.run(debug=True)