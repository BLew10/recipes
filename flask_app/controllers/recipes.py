# controllers.py, however many tables you have is however many controllers you need
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# controllers file name shoudl be plural
# model file name should be singular
#table_name is plural
#table_class is uppercase and singular
# table_name_singular represents the singular version of whatever the table is representing. Ex: Dojos -> dojo.

# route convention
# table_name/new -> displaying the form -> get method
# table_name/create -> processes form above -> post method
# table_name/<int:id> -> show -> get method
# table_name/<int:id>/edit -> displaying the form -> get method
# table_name/<int:id>/update -> processes the form -> post method
# table_name/<int:id>/delete-> deletes the row -> get method

@app.route('/recipe/new')
def recipe_new():
    return render_template("recipe_new.html")


@app.route('/recipe/create', methods=["post"])
def create_recipe():
    # creates a new __ from the client side and stores in the db
    if request.form['cook_time'] == 'yes':
        cook_time = 1
    else:
        cook_time = 0

    new_recipe_data = {
        "name": request.form['name'],
        "user_id": session['user_id'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "cook_time": cook_time,
        "created_at": request.form['created_at']
    }


    

    if not Recipe.validate_recipe(new_recipe_data):
        print(new_recipe_data)
        return redirect('/recipe/new')

    Recipe.create(new_recipe_data)
    print(new_recipe_data)
    return redirect('/dashboard')


@app.route('/recipe/<int:id>')
def recipe_show_one(id):

    recipe_id = {
        "id": id
    }

    live_user_id = {
        "id": session["user_id"]
    }
    # grabs all existing in the db
    recipe = Recipe.get_one(recipe_id)
    recipe_creator_id = recipe.user_id
    recipe_creator = User.get_one({"id": recipe_creator_id})

    live_user = User.get_one(live_user_id)
    return render_template("recipe_display.html", recipe=recipe, user=live_user, creator = recipe_creator)


@app.route('/recipe/<int:id>/edit')
def recipe_edit(id):
    recipe_id = {
        "id": id
    }
    # session['current_recipe'] = id
    # Recipe.update_recipe(recipe_id)
    recipe = Recipe.get_one(recipe_id)
    return render_template("recipe_edit.html", recipe=recipe)


@app.route('/recipe/<int:id>/update', methods=['POST'])
def update_recipe(id):
    # deletes the target instance

    if request.form['cook_time'] == 'yes':
        cook_time = 1
    else:
        cook_time = 0

    updated_recipe_data = {
        "id": id,
        "name": request.form['name'],
        "user_id": session['user_id'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "cook_time": cook_time,
        "created_at": request.form['created_at']
    }

    if not Recipe.validate_recipe(updated_recipe_data):
        return redirect('/recipe/<int:id>/edit')

    Recipe.update_recipe(updated_recipe_data)
    print(updated_recipe_data)
    return redirect('/dashboard')


@app.route('/recipe/<int:id>/delete')
def delete_recipe(id):
    # deletes the target instance
    deleted_recipe_data = {
        "id": id
    }
    Recipe.delete_recipe(deleted_recipe_data)
    print(deleted_recipe_data)
    return redirect("/")
