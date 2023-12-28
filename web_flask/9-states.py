#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Display a HTML page with a list of states."""
    states = storage.all("State")
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_detail(id):
    """Display a HTML page with details of a specific state."""
    state = storage.get("State", id)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        if hasattr(state, 'cities')
        else state.cities
        return render_template('state_detail.html', state=state, cities=cities)
    else:
        return render_template('not_found.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
