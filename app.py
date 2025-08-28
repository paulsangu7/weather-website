from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import os
import bcrypt
from dotenv import load_dotenv
from utils.weather_api import get_weather

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB setup
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.weather_app
users_collection = db.users

# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")
        if len(password) < 6:
            return render_template("signup.html", error="Password must be at least 6 characters")
        if users_collection.find_one({"email": email}):
            return render_template("signup.html", error="Email already registered")

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = {
            "username": username,
            "email": email,
            "password": hashed_pw,
            "search_history": []
        }
        users_collection.insert_one(user)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")

        user = users_collection.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            session["user"] = user["username"]
            session["email"] = user["email"]
            if remember:
                session.permanent = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid email or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if not session.get("email"):
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["email"]})
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if not session.get("email"):
        return redirect(url_for("login"))

    user = users_collection.find_one({"email": session["email"]})
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        old_pw = request.form.get("old_password")
        new_pw = request.form.get("new_password")
        confirm_pw = request.form.get("confirm_password")

        if not bcrypt.checkpw(old_pw.encode("utf-8"), user["password"]):
            return render_template("change_password.html", error="Old password incorrect")
        if new_pw != confirm_pw:
            return render_template("change_password.html", error="Passwords do not match")
        if len(new_pw) < 6:
            return render_template("change_password.html", error="New password must be at least 6 characters")

        hashed_pw = bcrypt.hashpw(new_pw.encode("utf-8"), bcrypt.gensalt())
        users_collection.update_one({"email": session["email"]}, {"$set": {"password": hashed_pw}})
        return render_template("change_password.html", success="Password updated successfully!")

    return render_template("change_password.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city")
    weather_data = get_weather(city)
    if not weather_data:
        return render_template("index.html", error="City not found!")
    if session.get("email"):
        users_collection.update_one(
            {"email": session["email"]},
            {"$push": {"search_history": city}}
        )
    return render_template("index.html", weather=weather_data)

@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
