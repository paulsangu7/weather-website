from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models.user import create_user, validate_user, find_user_by_email
from utils.weather_api import get_weather
from utils.agriculture_api import get_agriculture_data
from utils.geocode import get_lat_lon

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.weather_app
users_collection = db.users

# -----------------------------
# Authentication Routes
# -----------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")
        if len(password) < 6:
            return render_template("signup.html", error="Password too short")
        if find_user_by_email(email):
            return render_template("signup.html", error="Email already exists")
        create_user(username, email, password)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = validate_user(email, password)
        if user:
            session["email"] = user["email"]
            session["user"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():
    if not session.get("email"):
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["email"]})
    return render_template("dashboard.html", user=user)

# -----------------------------
# Weather Page (Home)
# -----------------------------
@app.route("/", methods=["GET", "POST"], endpoint="index")
@app.route("/weather", methods=["GET", "POST"], endpoint="weather")
def weather():
    weather_data = None
    city = None
    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather(city)
    return render_template("weather.html", weather=weather_data, city=city)

# -----------------------------
# Agriculture Page
# -----------------------------
@app.route("/agriculture", methods=["GET", "POST"])
def agriculture():
    if not session.get("email"):
        return redirect(url_for("login"))
    data = None
    if request.method == "POST":
        location = request.form.get("location")
        lat, lon = get_lat_lon(location)
        if lat is None or lon is None:
            data = {"error": "Could not find location"}
        else:
            data = get_agriculture_data(lat, lon)
            data["location_name"] = location.title()
    return render_template("agriculture.html", data=data)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
