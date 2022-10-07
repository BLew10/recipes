import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models.recipe import Recipe
from flask_app import app
# we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
bcrypt = Bcrypt(app)
# regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# model.py, however many tables you have is however many models you need

# Necessary if importing another Class to be referenced
# from flask_app.models import (child_model file)
# Example
# from flask_app.models.ninja import Ninja

# Things to change:
# Table_Class_Name
# (table_name) lowercase
# (table_name_singular) lowercase
# (scehma_name)

class User:
    # these should be the same as the columns in the table
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , password , created_at , updated_at ) VALUES (%(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"
        new_user_id = connectToMySQL('recipes_db').query_db(query, data)
        return new_user_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        # returns a list of dicts
        list_of_users_dicts_from_db = connectToMySQL(
            'recipes_db').query_db(query)
        # Create an empty list to append our instances of friends
        list_of_users_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for user_dict in list_of_users_dicts_from_db:
            list_of_users_instances.append(cls(user_dict))
        return list_of_users_instances

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        list_of_one_user_dict = connectToMySQL(
            'recipes_db').query_db(query, data)
        if not list_of_one_user_dict:
            return False
        return cls(list_of_one_user_dict[0])

    @classmethod
    def get_user_with_recipes(cls, data):
        query = 'SELECT * FROM users JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;'
        list_of_user_recipe_dicts = connectToMySQL(
            'recipes_db').query_db(query, data)

        if not list_of_user_recipe_dicts:
            return []

        user = cls(list_of_user_recipe_dicts[0])

        for recipe in list_of_user_recipe_dicts:
            if recipe['cook_time'] == 1:
                recipe['cook_time'] = "Yes"
            else:
                recipe['cook_time'] = "No"
                
            recipe_info = {
                "id" : recipe['recipes.id'],
                "name": recipe['name'],
                "description": recipe['description'],
                "instructions": recipe['instructions'],
                "cook_time": recipe['cook_time'],
                "created_at": recipe['created_at'],
                "updated_at": recipe['updated_at'],
                "user_id":  data['id']

            }
            user.recipes.append(Recipe(recipe_info))

        return user.recipes


    @classmethod
    def delete_user(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        user = connectToMySQL('recipes_db').query_db(query, data)
        return cls(user)

    @classmethod
    def update_user(cls, data):
        query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;'
        user = connectToMySQL('recipes_db').query_db(query, data)
        return cls(user)

    # IF EMAIL FOR USERS
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # returns a list of dicts
        list_dict_user_email = connectToMySQL(
            "recipes_db").query_db(query, data)
        # Didn't find a matching user
        if len(list_dict_user_email) < 1:
            return False
        return cls(list_dict_user_email[0])

    @staticmethod
    def validate_user(user):
        is_valid = True  # we assume this is true

        if len(user['first_name']) < 1:
            flash("Must input first name.", "registration")
            is_valid = False

        if len(user['last_name']) < 1:
            flash("Must input last name.", "registration")
            is_valid = False

        if len(user['password']) < 1:
            flash("Passwords needs to be longer than 1 characters", "registration")
            is_valid = False

        if user['password'] != user['confirm_password']:
            flash("Passwords do not match", "registration")         
            is_valid = False
        # test whether a field matches the pattern, email check for users
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "registration")
            is_valid = False

        return is_valid
