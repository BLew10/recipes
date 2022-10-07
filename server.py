
from flask_app.controllers import recipes
from flask_app.controllers import users
# Example
# from flask_app.controllers import dojos, ninjas
from flask_app import app

if __name__=="__main__":
    app.run(debug=True) 

# server imports controllers (routes).   the controllers (routes) import models (classes) that pertain to those routes. the models import your mysqlconnection config file so they can access the db with queries
