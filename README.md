# Flask Boilerplate for Profesional Development

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/from-referrer/)
<p align="center">
    <a href="https://youtu.be/ORxQ-K3BzQA"><img height="200px" src="https://github.com/4GeeksAcademy/flask-rest-hello/blob/main/docs/assets/how-to.png?raw=true?raw=true" /></a>
</p>

## Features

- Extensive documentation [here](https://github.com/4GeeksAcademy/flask-rest-hello/tree/master/docs).
- Integrated with Pipenv for package managing.
- Fast deloyment to heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.

## Installation (automatic if you are using gitpod)

> Important: The boiplerplate is made for python 3.7 but you can easily change the `python_version` on the Pipfile.

The following steps are automatically runned withing gitpod, if you are doing a local installation you have to do them manually:

```sh
pipenv install;
mysql -u root -e "CREATE DATABASE example";
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```

## How to Start coding?

There is an example API working with an example database. All your application code should be written inside the `./src/` folder.

- src/main.py (it's where your endpoints should be coded)
- src/models.py (your database tables and serialization logic)
- src/utils.py (some reusable classes and functions)
- src/admin.py (add your models to the admin and manage your data easily)

For a more detailed explanation, look for the tutorial inside the `docs` folder.

## Remember to migrate every time you change your models

You have to migrate and upgrade the migrations for every update you make to your models:
```
$ pipenv run migrate (to make the migrations)
$ pipenv run upgrade  (to update your databse with the migrations)
```


# Manual Installation for Ubuntu & Mac

⚠️ Make sure you have `python 3.6+` and `MySQL` installed on your computer and MySQL is running, then run the following commands:
```sh
$ pipenv install (to install pip packages)
$ pipenv run migrate (to create the database)
$ pipenv run start (to start the flask webserver)
```


## Deploy to Heroku

This template is 100% compatible with Heroku[https://www.heroku.com/], just make sure to understand and execute the following steps:

```sh
// Install heroku
$ npm i heroku -g
// Login to heroku on the command line
$ heroku login -i
// Create an application (if you don't have it already)
$ heroku create <your_application_name>
// Commit and push to heroku (commited your changes)
$ git push heroku main
```
:warning: For a more detailed explanation on working with .env variables or the MySQL database [read the full guide](https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/DEPLOY_YOUR_APP.md).


# Endpoints

## /register

```
This is a POST method, and this endpoint register a new user, with the following info:

{
    "email":"antonio@4geeks.com",
    "password": "123456",
    "is_active": true
}

if everything is correct, password should be encrypted in database, and you will get this message:

{
    "mensaje": "Usuario creado exitosamente"
}

```

## /login

```
Going to POSTMAN and make a POST method request to /login with following info at JSON, as example:

{
    "email":"antonio@4geeks.com",
    "password":"123456"
}

If everything is correct you'll get something like this:

{
    "access_token": "eyJ0eXA...eyJmcmVzaCI....-DJSyg2ygoQ6...-RkPdvIqdnAU..."
}

```

## Access to a protected endpoint: /people/<int:people_id>

```
Let say that you want access to information of character with people_id = 1.
You have to go to endpoint /people/1  
but it's protected, so you have to make login first to retrieve an access_token.

After that, go to POSTMAN, as this endpoint is a GET method, you don't have to fill body.
But, you must retrive information inside the Header, with Authorization and acces_token.

Add a new KEY as: Authorization
And add a new VALUE as: Bearer eyJ0eXA...eyJmcmVzaCI....-DJSyg2ygoQ6...-RkPdvIqdnAU...

If everything is ok, you will get an answer like:

{
    "description": "Jedi",
    "height": 2.0,
    "id": 1,
    "mass": 71.0,
    "name": "Luke Skywalker"
}

**Note: Database must have information**
```

## /favorite/people
```
This endpoint has a GET and POST methods. Post works to register a new favorite character to an user. And Get method works to retrieve information of all users and their favorite characters

example of GET method (check serialize() method to see how this work):

[
    {
        "id": 1,
        "people_name": "Luke Skywalker",
        "user_email": "antonio@4geeks.com"
    }
]


to Register, use POST Method with user_id and people_id as integers:

    {
        
        "people_id": 1,
        "user_id": 1
    }

```