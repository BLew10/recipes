# controllers.py, however many tables you have is however many controllers you need
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


#controllers file name shoudl be plural
#model file name should be singular
#table_name is plural
#table_class is uppercase and singular
#table_name_singular represents the singular version of whatever the table is representing. Ex: Dojos -> dojo. 

#route convention
#table_name/new -> displaying the form -> get method
#table_name/create -> processes form above -> post method
#table_name/<int:id> -> show -> get method
#table_name/<int:id>/edit -> displaying the form -> get method
#table_name/<int:id>/update -> processes the form -> post method
#table_name/<int:id>/delete-> deletes the row -> get method

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/user/create', methods=['POST'])
def register():
        
    if not User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    
    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # put the pw_hash into the data dictionary
    new_user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    # Call the save @classmethod on User
    user_id = User.create(new_user_data)
    # store user id into session
    session['user_id'] = user_id
    # ... do other things
    return redirect('/dashboard')


#for users
@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)

    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if not "user_id" in session:
        return redirect("/")
        
    user_id = {
        "id": session['user_id']
    }
    #grabs all user information, everything accessible in the db is now available for use
    user = User.get_one(user_id)
    print
    all_recipes = Recipe.get_all()

    for recipe in all_recipes:
        if recipe.cook_time == 1:
            recipe.cook_time = "Yes"
        else:
            recipe.cook_time = "No"

    return render_template("user_recipes.html", user = user, recipes = all_recipes )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')