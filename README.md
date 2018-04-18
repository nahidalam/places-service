# RESTful Service Google Maps Places API

##### This program extracts data from Google Maps Places API (nearby search). As a sample, I have extracted data for all the places within 500m radius of lattitude -33.8670522 and longitude 151.1957362. Portion of those data are stored in a persistent data store. If anyone queries for different types of places (e.g; food, car_rental, museum etc.), the program outputs information on all the places of that type (e.g; food, car_rental, museum etc.).

## How to Run:

Assuming you are running in a Mac environment

1. Download the code in YOUR_DIRECTORY
2. $cd YOUR_DIRECTORY
3. $ virtualenv flask
4. $ flask/bin/pip install flask
5. $ flask/bin/pip install requests
6. Make sure you have the right permission for the service $sudo chmod a+x places.py
7. $ ./places.py

This should run the service in localhost port 5000

## How to Use the Service API:

Paste below link in your browser

#### http://localhost:5000/places/api/v1.0/json?type=car_rental

You should see an output showing the Name, Lattitude, Longitude and Vicinity of all the car_rental places stored in the database.


## Further Improvements:

I have extracted data for all the places within 500m radius of lattitude -33.8670522 and longitude 151.1957362. These values can be auto generated for data scrapping through the API.

Right now, we have to enter the exact word such as 'car_rental' to find a place by type. If there is a typo, the service will not return any answer. To solve this, we can use Elasticsearch database which can automatically match similar words and return relevant results.  

One obvious Improvement is securing the RESTful web service. Right now, the service is open to public. One way to
secure it is to force login through username and password.
