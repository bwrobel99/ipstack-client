# ipstack-client

## Details
ipstack-client is a client of a popular API - IPStack.com. It is backed by a PostgreSQL database. Also, uses JWT authorization method, in accordance with OAuth2 password flow. 
Features:
 - RESTful API 
 - JWT authorization
 - IPStack API integration
 - Dockerized
 - deployed on Heroku: https://ipstack-client.herokuapp.com

The application is able to store geolocation data in the database, based on IP address or URL. You can use the API to add, delete or fetch geolocation data on the base of ip address or URL. 

## Run it locally
To run it, do:
```
docker-compose build
docker-compose run api initiate_db
docker-compose run api alembic upgrade head
docker-compose up
```
Please mind that you have to provide your IPStack API key by setting the `IPSTACK_API_KEY` variable. 

You should see that the app is running on port 8000.

## Docs
Interactive docs can be found here: https://ipstack-client.herokuapp.com/docs.
Available endpoints:

### /login
Input: username and password. 

Returns: {"access_token": `TOKEN`}

### /register
Input: username and password. 

Returns: User object

### /localizations
**PRIVATE ROUTE - JWT AUTH REQUIRED**. 

Returns all geolocalizations currently stored in the database.

### /localizations/check
**PRIVATE ROUTE - JWT AUTH REQUIRED**. 

Input: URL (*WITH SCHEMA!*), e.g. `http://example.com` 

Returns geolocalization info for provided address (URL or IP). If info for this address is present in the db, this info is returned. Otherwise, info fetched from IPStack's API is returned. If no info is found, null is returned.

### /localizations/add
**PRIVATE ROUTE - JWT AUTH REQUIRED**. 

Input: JSON( {"address": `http://example.com`} ) 

Fetches geolocalization info for the provided address (URL or IP, inside a JSON body), saves it in the db, and returns it. If an entry for the provided address already exists, it is overwritten.

### /localizations/delete
**PRIVATE ROUTE - JWT AUTH REQUIRED**. 

Input: JSON( {"address": `http://example.com`} ) 

Deletes geolocalization info for the provided address (URL or IP, inside a JSON body) from the db.
