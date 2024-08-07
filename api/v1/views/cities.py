#!/usr/bin/python3
'''cities module'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCity(city_id=None):
    '''get a city by id'''
    if city_id is None:
        abort(404)
    cty = storage.get(City, city_id)
    if cty is None:
        abort(404)
    return jsonify(cty.to_dict())


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def getCitiesInState(state_id=None):
    '''gets all cities in state with their id passed'''
    if state_id is None:
        abort(404)
    sty = storage.get(State, state_id)
    if sty is None:
        abort(404)
    ctys = sty.cities
    return jsonify([cty.to_dict() for cty in ctys])


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id=None):
    '''deletes a city'''
    if city_id is not None:
        result = storage.get(City, city_id)
        if result is not None:
            storage.delete(result)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def postCity(state_id=None):
    '''posts a new city to a specific state'''
    if state_id is None:
        abort(404)
    sty = storage.get(State, state_id)
    if sty is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body.keys():
        abort(400, 'Missing name')
    body['state_id'] = st.id
    obj = City(**body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id=None):
    '''updates a city'''
    if city_id is None:
        abort(404)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
