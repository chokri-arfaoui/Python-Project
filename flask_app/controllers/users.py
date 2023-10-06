from flask import render_template, request, redirect, session, flash, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.request import Request
from flask_app.models.response import Response
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# __________________ INDEX _______________________


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup')
def login2():
    return render_template("signup.html")
# ___________________SIGNUP_______________________


# @app.route('/users/create', methods=['POST'])
# def create_user():
#     form_data = {
#         'first_name': request.form['first_name'],
#         'last_name': request.form['last_name'],
#         'email': request.form['email'],
#         'password': request.form['password'],
#         'confirm_password': request.form['confirm_password'],
#         'role': request.form['role'],  # Retrieve the selected role value
#     }
#     print(form_data)

#     if User.validate(form_data):
#         User.create(form_data)
#         return redirect('/login')
#     # return redirect('/')  # Redirect back to the signup page

# @app.route('/signup')
# def signup():
#     return render_template("signup.html")

# ___________________LOGIN_________________________
@app.route("/login", methods=["POST"])
def login12():
    user = User.get_by_email({"email": request.form["email"]})
    if not user:
        flash("Invalid Email / Password", "login")
        return redirect("/login")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid Email / Password", "login")
        return redirect("/login")
    session["user_id"] = user.id
    if user.role == "chef" :
        return redirect("/chef_dashboard")
    elif user.role == "admin" :
        return redirect("/dashboard_admin")
    else :
        return redirect("/client_dash")
    
    
@app.route('/login')
def login():
    return render_template("login.html")


# _________________________________________________
@app.route('/chefs')
def chefs():
    return render_template("chefs.html")

@app.route('/food_menu')
def food_menu():
    return render_template("food_menu.html")

@app.route('/request_recipe')
def request_recipe():
    # ///////////
    chefs = User.get_chefs()
    return render_template("request_recipe.html",chefs=chefs)

@app.route('/get_chefs_by_dish', methods=['POST'])
def get_chefs_by_dish():
    selected_dish = request.form['selected_dish']

    # Call your User.get_chefs method with the selected dish as an argument
    chefs = User.get_chefs(food_type=selected_dish)

    # Create a list of chef dictionaries with 'id' and 'name' keys
    chef_list = [{'id': chef.id, 'name': f'{chef.first_name} {chef.last_name}'} for chef in chefs]

    return jsonify(chefs=chef_list)

@app.route('/chef_dashboard')
def chef_dashboard():
    reqs=Request.get_by_chefid({"chef_id": session['user_id']})
    return render_template("chef_dashboard.html",requests=reqs)

@app.route('/my_recipe/<req_id>')
def my_recipe(req_id):
    recipes=Recipe.get_recipes_by_reqid({'request_id':req_id})
    return render_template("my_recipe.html",recipes=recipes)

@app.route('/client_dash')
def client_d():
    reqs=Request.get_by_userid({"custumer_id": session['user_id']})
    return render_template("client_dashboard.html",requests=reqs)

@app.route('/form_chef')
def form_chef():
    return render_template("form_chef.html")

@app.route('/dashboard_admin')
def dashboard_admin():
    chefs= User.get_chefs()
    return render_template("dashboard_admin.html",chefs=chefs)

# ----------------- delete chef ----------------------
@app.route('/chef/<chef_id>/destroy/')
def delete_chef(chef_id):
    User.delete({'id':chef_id})
    return redirect('/dashboard_admin')

@app.route('/send_recipe/<req_id>')
def send_recipe(req_id):
    one_req=Request.get_by_id({'id':req_id})
    return render_template("send_recipe.html",req=one_req)


#     logged_user = User.get_by_id({'id':session['user_id']})
#     recipes = Recipe.get_all()
#     return render_template("recipes.html", user = logged_user, recipes = recipes)

@app.route('/users/create', methods=['POST'])
def register():

    if(User.validate(request.form)):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            **request.form,'password':pw_hash
        }
        user_id = User.create(data)
        session['user_id'] = user_id
        user = User.get_by_email({"email": request.form["email"]})
        if user.role == "chef" :
            return redirect("/form_chef")
        else :
            return redirect("/client_dash")
    return redirect('/signup')

@app.route('/requests/create', methods=['POST'])
def add_req():

    data = {
        **request.form,'custumer_id':session["user_id"],'status':"pending"
    }
    print(data)

    req_id = Request.create(data)
    return redirect('/client_dash')

@app.route('/recipes/create', methods=['POST'])
def add_recip():

    data = {
        **request.form,'chef_id':session["user_id"]
    }
    print(data)
    recip_id = Recipe.create(data)
    # add response link
    Response.create({"recipe_id": recip_id,"request_id":data['request_id']})
    # change request status to completed
    Request.edit({"id":data['request_id'],"status":"Completed"})
    return redirect('/chef_dashboard')
    

@app.route('/users/add_food_type', methods=['POST'])
def add_food():
    
    User.set_food_type({"id": session['user_id'],"food_type":request.form["food_type"]})
    return redirect("/chef_dashboard")





@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')