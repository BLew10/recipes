from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt    
from flask_app import app    
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
#regex 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 




# model.py, however many tables you have is however many models you need

#Necessary if importing another Class to be referenced 
# from flask_app.models import (child_model file)
# Example
# from flask_app.models.ninja import Ninja

# Things to change:
# Table_Class_Name
# recipes lowercase
# recipe lowercase
# (scehma_name)


class Recipe:
    #these should be the same as the columns in the table
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cook_time = data['cook_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # We create a list so that later we can add in all the burgers that are associated with a restaurant.
        # self.ninjas = []

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO recipes ( name , description , instructions , cook_time, user_id, created_at, updated_at ) VALUES (%(name)s, %(description)s , %(instructions)s , %(cook_time)s , %(user_id)s, %(created_at)s , NOW());"

        # users query
        # query = "INSERT INTO users (username, password) VALUES (%(username)s, %(password)s);"
        new_recipe_id = connectToMySQL('recipes_db').query_db(query, data)
        return new_recipe_id
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        #returns a list of dicts
        list_of_recipes_dicts_from_db = connectToMySQL('recipes_db').query_db(query)

        if not list_of_recipes_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_recipes_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe_dict in list_of_recipes_dicts_from_db:
            list_of_recipes_instances.append(cls(recipe_dict))
        return list_of_recipes_instances

    @classmethod
    def get_one(cls, data:dict):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        list_of_one_recipe_dict = connectToMySQL('recipes_db').query_db(query, data)
        if not list_of_one_recipe_dict:
            return False
        return cls(list_of_one_recipe_dict[0])

    @classmethod
    def delete_recipe(cls, data:dict):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        recipe = connectToMySQL('recipes_db').query_db(query, data)
        return cls(recipe)

    @classmethod
    def update_recipe(cls, data:dict):
        query = 'UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, cook_time = %(cook_time)s, updated_at = NOW()  WHERE id = %(id)s;'
        recipe = connectToMySQL('recipes_db').query_db(query, data)
        return recipe

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True  # we assume this is true

        if len(recipe['name']) < 1:
            flash("Put in a name.", "recipe")
            is_valid = False

        if len(recipe['description']) < 1:
            flash("Put in a description.", "recipe")
            is_valid = False

        if not recipe['instructions']:
            flash("Bruh you aint gonna tell me how to do it?", "recipe")
            is_valid = False

        if not "cook_time" in recipe:
            flash("Put in a cook time", "recipe")
            is_valid = False

        if not "created_at" in recipe:
            flash("Put in a date created", "recipe")
            is_valid = False

        return is_valid

