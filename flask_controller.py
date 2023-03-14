from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from yeelight_controller import *
from pymongo_get_database import get_database   

app = Flask(__name__)
app.secret_key = "secret_key"

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"<User {self.id}>"

# User database
users = {"user1": {"id": "user1", "password": "password1"}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        if user_id in users and password == users[user_id]["password"]:
            user = User(user_id)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password"
    return render_template("login.html")

@app.route("/dashboard",methods=["GET", "POST"])
def dashboard():
    state = get_bulb_properties('192.168.2.209')['power']
    print(state)
    if state == 'on':
       light_on = True
    if current_user.is_authenticated:
        return render_template("dashboard.html", light_on=light_on)
    else:
        return redirect(url_for("login"))


@app.route("/switch-lights", methods=["POST"])
def switch_lights():
    state = request.json.get('state')
    print(request.json)
    if state == 'on':
       turn_on_bulb('192.168.2.209')
    else:
       turn_off_bulb('192.168.2.209')    
    return ""    
# @app.route("/<>/turn_off_bulb")
# def dashboard():
#     if current_user.is_authenticated:
#         return render_template("dashboard.html")
#     else:
#         return redirect(url_for("login"))    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    ybulbs = discover_bulbs()
    
    app.run(debug=True)
