from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from yeelight_controller import *
from pymongo_get_database import get_database   

app = Flask(__name__)
app.secret_key = "secret_key"
db = get_database()
collection = db['Yeelight-bulbs']
lights= []

class Light:
    def __init__(self,id,ip,bulb_type,state,brightness,color):
        self.id = id
        self.ip = ip
        self.bulb_type = bulb_type
        self.state = state
        self.brightness = brightness
        self.color = color
    def __str__(self):
        return f"Light(id='{self.id}', ip='{self.ip}', bulb_type='{self.bulb_type}', brightness='{self.brightness}', color='{self.color}')"    



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
    
    #print(ybulbs)
    for ybulb in ybulbs:
        light = Light(ybulb['capabilities']['id'],ybulb['ip'],'yeelight',ybulb['capabilities']['power'],ybulb['capabilities']['bright'],ybulb['capabilities']['rgb'])
        lights.append(light)
    
    
    #state = get_bulb_properties('192.168.2.209')['power']
    #print(state)
    
    if current_user.is_authenticated:
        return render_template("dashboard.html", lights=lights)
    else:
        return redirect(url_for("login"))


@app.route("/switch-lights", methods=["POST"])
def switch_lights():
    if current_user.is_authenticated:    
        state = request.json.get('state')
        ip = request.json.get('ip')
        print(request.json)
        if state == 'on':
         turn_on_bulb('192.168.2.209')
        else:
         turn_off_bulb('192.168.2.209')
        return "Triggered"       
    else:
        return redirect(url_for("login"))     
     
       

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    #ybulbs = [{'ip': '192.168.2.209', 'port': 55443, 'capabilities': {'id': '0x00000000155d5e79', 'model': 'strip6', 'fw_ver': '20', 'support': 'get_prop set_default set_power toggle set_bright set_scene cron_add cron_get cron_del start_cf stop_cf set_name set_adjust adjust_bright set_ct_abx adjust_ct adjust_color set_rgb set_hsv set_music udp_sess_new udp_sess_keep_alive udp_chroma_sess_new', 'power': 'on', 'bright': '1', 'color_mode': '3', 'ct': '3200', 'rgb': '2366719', 'hue': '242', 'sat': '89', 'name': ''}}, {'ip': '192.168.2.106', 'port': 55443, 'capabilities': {'id': '0x00000000158af61f', 'model': 'color4', 'fw_ver': '39', 'support': 'get_prop set_default set_power toggle set_bright set_scene cron_add cron_get cron_del start_cf stop_cf set_ct_abx adjust_ct set_name set_adjust adjust_bright adjust_color set_rgb set_hsv set_music udp_sess_new udp_sess_keep_alive udp_chroma_sess_new', 'power': 'off', 'bright': '75', 'color_mode': '2', 'ct': '2635', 'rgb': '16765825', 'hue': '39', 'sat': '49', 'name': ''}}]
    ybulbs = discover_bulbs()
    print(ybulbs)
    for bulb in ybulbs:
     query = {'id': bulb['capabilities']['id']}
     update = {'$set': bulb}
     collection.update_one(query, update, upsert=True)
    ybulbs= list(collection.find())
    print(ybulbs)
    app.run(debug=True)
