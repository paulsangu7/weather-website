from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from functools import wraps

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
# Helper: Login Required Decorator
# -----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("email"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

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
@login_required
def dashboard():
    user = users_collection.find_one({"email": session["email"]})
    return render_template("dashboard.html", user=user)

# -----------------------------
# Weather Page (Home)
# -----------------------------
@app.route("/", methods=["GET", "POST"], endpoint="index")
@app.route("/weather", methods=["GET", "POST"], endpoint="weather")
@login_required
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
@login_required
def agriculture():
    data = None
    recommendation = None

    if request.method == "POST":
        location = request.form.get("location")
        weather_data = get_weather(location)  # same weather API used by Weather page

        if not weather_data:
            data = {"error": "Could not retrieve weather for this location"}
        else:
            data = weather_data
            condition = weather_data.get("condition", "").lower()
            temp = weather_data.get("temperature")
            humidity = weather_data.get("humidity")
            rain = weather_data.get("rain", 0)

            # Detailed English recommendation
            if "rain" in condition or rain > 2:
                recommendation = (
                    "The weather indicates rainfall. This is ideal for water-intensive crops "
                    "like rice, leafy vegetables, and maize. Ensure proper drainage to prevent waterlogging."
                )
            elif temp and temp > 30:
                recommendation = (
                    f"The temperature is high ({temp}°C). Plant drought-resistant crops such as cassava, millet, "
                    "or sorghum. Mulching is recommended to retain soil moisture."
                )
            elif temp and temp < 18:
                recommendation = (
                    f"Cool temperatures ({temp}°C) are observed. Consider planting crops tolerant to cold "
                    "such as potatoes, carrots, and leafy greens. Protect seedlings from frost if necessary."
                )
            else:
                recommendation = (
                    f"The weather is moderate ({temp}°C, Humidity: {humidity}%). You can safely plant "
                    "common crops like maize, beans, cowpeas, or vegetables. Ensure regular monitoring of soil moisture."
                )

    return render_template("agriculture.html", data=data, recommendation=recommendation)


# -----------------------------
# Health Check (No login required)
# -----------------------------
@app.route("/health")
def health_check():
    return "OK", 200

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
