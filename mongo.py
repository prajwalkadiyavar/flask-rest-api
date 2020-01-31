from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.camera    

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'camera'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/camera'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def get_all_stars():

  output = []
  for s in db.cone.find():
    output.append({'name' : s['name'], 'age' : s['age']})
  return jsonify({'result':True,"response" : output})

@app.route('/name', methods=['GET'])
def get_one_name():
	output = []
	if request.method == 'GET':
		jsonobject=request.json
		nam=jsonobject['name']
		for s in db.cone.find():
			if(s['name']==nam):
				output.append({'name' : s['name'], 'age' : s['age']})
		return jsonify({'result' : output})
@app.route('/age', methods=['GET'])
def get_one_age():
	output = []
	if request.method == 'GET':
		jsonobject=request.json
		ag=jsonobject['age']
		for s in db.cone.find():
			if(s['age']==ag):
				output.append({'name' : s['name'], 'age' : s['age']})
		return jsonify({'result':True,'response' : output})
 

@app.route('/add', methods=['POST'])
def add_std():
	jsonobject=request.json
	nam = jsonobject['name']
	ag = jsonobject['age']
	if(db.cone.find_one({'name': nam, 'age': ag})):
		return jsonify({'result' : False,"response:":"Failed -- Person already exists --"})
	else:
		db.cone.insert_one({'name': nam, 'age': ag})
		return jsonify({'result' : True,"response:": " Record Added"})
@app.route('/upd', methods=['PUT'])
def upd_std():
	jsonobject=request.json
	nam = jsonobject['name']
	ag = jsonobject['age']
	
	db.cone.find_one_and_update({'name': nam},{'$set': {"age":ag}}, upsert=True)
	ss=db.cone.find_one({'name': nam})
	return jsonify({'result' : True,'response': " --Updated --","record ":str(ss)})
	






@app.route('/delet', methods=['POST'])
def del_std():
	jsonobject=request.json
	nam = jsonobject['name']
	ag = jsonobject['age']
	j=db.cone.find_one({'name': nam})
	v=db.cone.find_one({'age': ag})
	ss=str(j)
	vv=str(v)
	if(j):
		db.cone.delete_one({'name': nam})
		return jsonify({'result' : True,'response': " -- Record Deleted --","Record":ss})
	elif(v):
		db.cone.delete_one({'age': ag})
		return jsonify({'result' : True,'response': " -- Record Deleted --","Record":vv})

	else:
		return jsonify({'result' : False,'response': " -- Person Doesn't exists --"})
		
		






if __name__ == '__main__':
    app.run(debug=True)
