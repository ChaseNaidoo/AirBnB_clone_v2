#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display a HTML page like 8-index.html from the AirBnB clone project."""
    states = storage.all("State")
    cities = storage.all("City")
    amenities = storage.all("Amenity")
    places = storage.all("Place")

    return render_template(
        '100-hbnb.html',
        states=states,
        cities=cities,
        amenities=amenities,
        places=places
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
