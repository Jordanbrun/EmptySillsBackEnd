import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict
from shamrock import Shamrock
import requests
import datetime
from flask_cors import CORS

plant = Blueprint('plants', 'plant')
CORS(plant)



#List all plants associated with user
@plant.route('/', methods=['GET'])
def list_plants():
	print(current_user)
	try:
		plants = [model_to_dict(d) for d in models.Plant.select()]
		return jsonify(data=plants, status={'code': 200, 'message': 'Success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})


#List individual plant based on ID
@plant.route('/<plant_id>/', methods=['GET'])
def get_plant(plant_id):
	plant = model_to_dict(models.Plant.get(id=plant_id))
	return jsonify(plant)


#Search route for querying the API
@plant.route('/search/', methods=['POST'])
def search_plant():
	print("before plant")
	queryPlant = []
	api = Shamrock('eTdMWkZzcGdZenh4c2NadEFtR0pLZz09')
	payload = request.get_json();
	value = payload['userInput']
	allPlants = api.plants()
	returnedPlant = api.search(value);
	print(returnedPlant)
	for plant in returnedPlant:
		id = plant.get("id", "")
		print(id, "this in the print thing yo")
		plantDetails = api.plants(id)
		queryPlant.append(plantDetails)
		print(queryPlant)
	return jsonify(queryPlant);

@plant.route('/sill/', methods=['POST'])
def search_users_plant():
	print("before plant")
	api = Shamrock('eTdMWkZzcGdZenh4c2NadEFtR0pLZz09')
	payload = request.get_json();
	print(payload)
	allPlants = api.plants(payload)
	print(allPlants)
	return jsonify(allPlants);

#create plant
@plant.route('/', methods=['POST'])
def create_plant():
	try:
		payload = request.get_json()
		print(payload, "0")
		payload['user'] = current_user.id
		print(payload, "1")
		created_plant = models.Plant.create(**payload)
		print(create_plant, "2")
		created_plant_dict = model_to_dict(created_plant)
		print(created_plant_dict, "3")
		return jsonify(data=created_plant_dict, status={'code': 201, 'message': 'success'})
	except:
		 print("error in create_plant")


#Delete plant
@plant.route('/<id>/', methods=['DELETE'])
def delete_plant(id):
	query = models.Plant.delete().where(models.Plant.id==id)
	query.execute()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

#Edit Route
@plant.route('/<id_plant>/', methods=['PUT'])
def update_plant(id_plant):
	print(id_plant)
	models.Plant.update(
		last_watered=datetime.datetime.now()
	).where(models.Plant.id==id_plant).execute()
	updated_plant = models.Plant.get(id = id_plant)
	update_plant_dict = model_to_dict(updated_plant)
	print(updated_plant)
	return jsonify(data=update_plant_dict, status={'code': 200, 'message': 'success'})




