#!flask/bin/python

'''
Author: Nahid Alam
RESTful service using Python
'''

from flask import Flask, jsonify
from flask import make_response
from flask import abort
from flask import request
import os
import sys
import json, urllib
from pprint import pprint
import requests
from CONFIG import *

app = Flask(__name__)


import sqlite3


# SQL command to create a table in the database
command_create_table = """CREATE TABLE if not exists place (
name VARCHAR(100),
lat DOUBLE(100, 10),
lng DOUBLE(100,10),
vicinity VARCHAR(100),
typeOfPlace VARCHAR(100));"""

def findGeoData(lat, lon, radius):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(lat) +','+str(lon)+ '&radius='+str(radius)+ '&key=' + APIKey
    response = urllib.urlopen(url)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    return jsonData

def storeData(data):
    #parse the data, store based on name - store lat, lng, vicinity, type
    print("storing")
    connection = sqlite3.connect("places.db")

    cursor = connection.cursor()

    cursor.execute(command_create_table)

    for item in data["results"]:
        name = item["name"]
        lat = item["geometry"]["location"]["lat"]
        lng = item["geometry"]["location"]["lng"]
        vicinity = item['vicinity']
        typeOfPlace = item['types'][0]
        cursor.execute("INSERT or IGNORE into place (name, lat, lng, vicinity, typeOfPlace) values (?, ?, ?, ?, ?)",(name, lat, lng, vicinity, typeOfPlace))

    connection.commit()
    connection.close()

#RESTful Service interface
@app.route('/')
def index():
    return "Nearby Search RESTful Service"

@app.route('/places/api/v1.0/json',methods=['GET'])
def getTypes():
    #show all types from the database
    if 'type' in request.args:
        typeVar = request.args['type']
        connection = sqlite3.connect("places.db")

        cursor = connection.cursor()
        cursor.execute("SELECT * from place WHERE typeOfPlace=?", (typeVar,))
        ans= cursor.fetchall()


        line_items = []
        for row in ans:
            name = row[0]
            lat = row[1]
            lng = row[2]
            visinity = row[3]

            myJSON = {
            'name':name,
            'lat':lat,
            'lng':lng,
            'visinity':visinity
            }
            line_items.append(myJSON)
    #return jsonify(json.dumps(line_items))
    return json.dumps(line_items)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    #extract data for all the places within 500m radius of lattitude -33.8670522 and longitude 151.1957362
    data = findGeoData(-33.8670522,151.1957362, 500)
    if data['results'] !=None:
        #store data in a SQL database
        storeData(data)
    app.run(debug=True)
