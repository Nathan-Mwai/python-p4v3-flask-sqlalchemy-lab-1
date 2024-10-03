# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakes(id):
    # earthquake = [{
    #     "id": quake.id,
    #     "location": quake.location,
    #     "magnitude": quake.magnitude,
    #     "year": quake.year
    # } for quake in Earthquake.query.filter(Earthquake.id == id)]
    # if earthquake:
    #     return make_response(earthquake, 200)
    # else:
    #     return {
    #         "message": f"Earthquake {id} not found."
    #     }
    # PYTEST REFUSED FIRST OPTION
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        response = make_response(
            {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year,
            },
            200,
        )
    else:
        response = make_response({"message": f"Earthquake {id} not found."}, 404)
    return response

@app.route('/earthquakes/magnitude/<float:magnitude>')
def find_magnitudes(magnitude):
    magnitudes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    response = {
        "count": len(magnitudes),
        "quakes": [{
            "id": eqs.id,
            "location": eqs.location,
            "magnitude": eqs.magnitude,
            "year": eqs.year
        } for eqs in magnitudes]
    }
    return make_response(response,200)
        
if __name__ == '__main__':
    app.run(port=5555, debug=True)
