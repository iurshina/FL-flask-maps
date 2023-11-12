# Flask / PostGres app template

## What is this template for?

As part of our course, we want to build a location-based web application. We know we will need a database to store some data, and that we want special support for geospatial data (latitude and longitude storage, searches based on distance, etc).

This teamplate is a guide on how to setup your application.
You can clone / fork this repo to get the contents of some of the files, but otherwise, you will not build directly on top of this.

Also, through this guide:

- The template includes sample code to show a Google Map and some markers in it
- The template also includes a sample model with some prestored locations, just to test out the map functionality and make sure PostGis extension works too.

The idea is you use this to get a first working version of these basic functionalities, and then start changing things to build your own app.

## Prerequisites

- A GitHub account and a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) so you can commit stuff from the command line
- Git installed in your machine so you can execute git commands
- Python installed in your machine so you can execute Python commands and run Pyton scripts. Make sure you have version **3.6 or superior**. You also need to use pip, can't remember if that needed to be installed separately.
- A Google Maps API Key
- A local installation of [Postgres](https://www.postgresql.org/download/)

```bash
brew install postgresql@14
```

## Fork the project

Create a Python virtual environment:

**Mac / Linux**

```
python3 -m venv venv
. venv/bin/activate
```

**Windows**
You need to figure out [where is your Python executable](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html#where-is-python) first, that for me is (you will at least have to put your own username there instead of <username>):

```
virtualenv --python C:\Users\<username>\AppData\Local\Programs\Python\Python39\python.exe venv
.\venv\Scripts\activate
```

## Installing Dependencies

```
pip install -r requirements.txt
```

## Install PostGres

**Mac**

install

```bash
brew install postgresql@14
```

start
`brew services start postgresql@14`
stop
`brew services stop postgresql@14`

to create a database

`createdb <database_name>`

after this, you can connect to the database using PostgreSQL interactive terminal (psql). 

`psql -d <database_name>`

in the terminal, you can run SQL commands:

```sql
CREATE DATABASE <database_name>;
```

## Install postgis
PostGIS is an open-source extension for the PostgreSQL relational database management system that adds support for geographic and spatial data. It enables PostgreSQL to store, query, and manipulate geospatial data, such as points, lines, polygons, and more. PostGIS provides a wide range of functions and features for geospatial analysis, including proximity searches, distance calculations, spatial joins, and map overlays. This extension is widely used in various applications, such as geographic information systems (GIS), mapping, and location-based services, where the storage and analysis of geographic data are essential. PostGIS is a valuable tool for managing and extracting insights from spatial information within a relational database environment.

```bash
brew install postgis
```

to create a postgis extension

```sql
CREATE EXTENSION postgis;
```

## Running the app locally

- DATABASE_URL: this is the connection string for the PostGres database.
  set postgress URI in terminal, do this every time you run the app
  `export DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>`

- GOOGLE_MAPS_API_KEY: You need to get this for yourself (via the Google app console). It will be sent to the Google Maps API to render the map on the initial page of the sample app.
  set google maps api in terminal do this every time you run the app
  `export GOOGLE_MAPS_API_KEY=<api_key>`

:eight_pointed_black_star: The environment variables you are setting now only 'exist' for as long as you keep the terminal / Powershell session open. When you close it and start again, the variables are gone, and you have to set them again! So you will do this step every time you start working on your app.

For the value for GOOGLE_MAPS_API_KEY you need to get the real api key value from your Google Apps console and use that value instead.
Remember never to commit this API key to your repo because that is public and the key could get exploited / used by other people. Use of Google Maps API costs money after some limits, so be careful. If you publish your key by mistake you can invalidate it and create a new one.

If you want to verify the values of the env variables, use:

**Mac / Linux**

```
echo $DATABASE_URL
echo $GOOGLE_MAPS_API_KEY
```

**Windows / Option 1**

```
echo %DATABASE_URL%
echo %GOOGLE_MAPS_API_KEY%
```

**Windows / Option 2**

```
$env:DATABASE_URL
$env:GOOGLE_MAPS_API_KEY
```

Finally, to run the app:

**Mac / Linux / Windows **

```
flask run
```

You should see something like this on the output of the console:

```
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

If you access `http://127.0.0.1:5000/` or `http://localhost:5000/` you should see:

![sample app](/_readme_assets/Sample-app.png)

Bonus: during development, you normally want to reload your application automatically whenever you make a change to it. You can do this by passing an environment variable, FLASK_ENV=development, to flask run:

```
FLASK_ENV=development flask run
```

Use Ctrl+C to quit / shut down the flask app.

Happy coding!
