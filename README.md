 Weather Website 🌤️

## Description
Weather Website ni app ya kisasa inayowezesha watumiaji kuangalia hali ya hewa kwa city au country yoyote. Inajumuisha:  

- Login / Signup authentication  
- Dashboard kwa watumiaji kuangalia search history  
- Change password functionality  
- Sticky footer yenye social media links  
- Real-time weather data kutoka OpenWeatherMap API  

---

## Features
- Search weather by city or country  
- User authentication (Login & Signup)  
- Dashboard with user info and search history  
- Change password functionality  
- Save last searched locations  
- Sticky footer with links to Facebook, Twitter, Instagram, LinkedIn, GitHub  
- Responsive design using Bootstrap  

---

## Tech Stack
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript  
- Backend: Python, Flask  
- Database: MongoDB  
- API: OpenWeatherMap API  

---

## Installation

1. Clone repository  
```bash
git clone https://github.com/yourusername/weather-website.git
cd weather-website
````

2. Create virtual environment

```bash
python -m venv venv
```

3. Activate virtual environment

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Setup environment variables
   Create a `.env` file:

```
SECRET_KEY=your_flask_secret_key
MONGODB_URI=your_mongodb_uri
OPENWEATHERMAP_API_KEY=your_api_key
```

6. Run server

```bash
python app.py
```

---

## Usage

1. Open browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
2. Signup for an account or login if you already have one
3. Search for weather by city/country
4. Access your Dashboard to see search history
5. Change your password via Change Password page

---

## Folder Structure

```
weather-website/
├── app.py
├── .env
├── models/
│   └── user.py
├── utils/
│   └── weather_api.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── change_password.html
└── static/
    └── css/
        └── style.css
```

---

## Contributing

1. Fork the repository
2. Create a new branch: git checkout -b feature-name
3. Make changes and commit: git commit -m "Add feature"
4. Push to branch: git push origin feature-name
5. Open a pull request

---

## License

This project is licensed under the MIT License.

---

## Author / Credits

* Paulo Kiwaile
* GitHub: [https://github.com/pkiwalile](https://github.com/paulsangu7)
* LinkedIn: [https://www.linkedin.com/in/paulo-kiwalile-a32a1320a/](https://www.linkedin.com/in/paulo-kiwalile-a32a1320a/)

---

Optional Enhancements:

* Add build status, Python version badges
* Include GIF or screenshots of app in action
* Extend app features: dark mode, additional API data

