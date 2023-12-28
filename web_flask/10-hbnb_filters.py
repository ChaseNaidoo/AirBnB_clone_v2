#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display a HTML page like 6-index.html from the AirBnB clone project."""
    states = storage.all("State")
    cities = storage.all("City")
    amenities = storage.all("Amenity")

    return render_template(
        '10-hbnb_filters.html',
        states=states,
        cities=cities,
        amenities=amenities
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
