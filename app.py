
################################################## Dependencies and Setup #########################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

################################################## Database Setup #################################################

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True) 


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


################################################## Flask Setup #################################################
app = Flask(__name__)

################################################## Flask Routes #################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of dates and corresponding precipitations"""

    # Query precipitation from last year

    query_date =   '2016-08-23'
    Last12_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    return jsonify(Last12_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a dictionary of dates and corresponding tobs"""

    # Query tobs from last year

    query_date = '2016-08-23'  
    Last12_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).all()
    return jsonify(Last12_tobs)


if __name__ == '__main__':
    app.run(debug=True)