# Weather & Agriculture App

## Overview
This web application provides real-time weather information and agriculture insights for any location. Users can check the weather, get suggested crops based on current conditions, and manage their profiles. The app also features user authentication, a modern interface, and social media links in a sticky footer.

---

## Features
- User Authentication: Signup, Login, Logout.
- Weather Information: Displays temperature, humidity, wind speed, and weather condition.
- Agriculture Insights: Suggests crops based on location weather data.
- Dashboard: Personalized greeting with user’s first name and app instructions.
- Navigation: Navbar for easy access to Weather and Agriculture pages.
- Sticky Footer: Contains social media links (GitHub, X/Twitter, Facebook, LinkedIn, Instagram).
- Responsive Design: Works on desktops, tablets, and mobile devices.
- Interactive Elements: Hover effects on buttons and social media icons.

---

## Installation

1. Clone the repository 
```bash
git clone <your-repo-url>
cd weather-website
````

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables
   Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your_secret_key
MONGODB_URI=your_mongodb_uri
WEATHER_API_KEY=your_weather_api_key
```

5. Run the application

```bash
python app.py
```

The app will run on `http://127.0.0.1:5000/`.

---

## Usage

1. Open the app in your browser.
2. Login** or Signup to access the dashboard.
3. Use the Weather page to search for a city and view weather details.
4. Use Agriculture Insights to get crop recommendations based on location weather.
5. Use the navbar or the logo to navigate between pages.
6. Social media links are located at the footer.

---

## Project Structure

```
weather-website/
│
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── templates/
│   ├── base.html
│   ├── weather.html
│   ├── agriculture.html
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
├── static/
│   ├── logo.png
│   └── icons/               # Social media icons
├── models/
│   └── user.py
└── utils/
    ├── weather_api.py
    ├── agriculture_api.py
    └── geocode.py
```

---

## Notes

* Ensure MongoDB is running and accessible via `MONGODB_URI`.
* API keys must be valid for weather and agriculture data.
* Users cannot access weather or agriculture pages without logging in.
* Responsive design uses Flexbox and CSS media queries.
* Social media icons are white with hover effects.

---

## License

This project is open for modification and personal use.