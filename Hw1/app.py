from flask import Flask, render_template, request
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import HTTPError
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"
OPEN_WEATHER_KEY = '419ec15e612827a933c48861193ee6bf'

COVID_API_URL = "https://newsapi.org/v2/top-headlines?q=covid&language=en&sortBy=publishedAt&apiKey={}"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?q={0}&language=en&sortBy=publishedAt&page=1&apiKey={1}"
NEWS_API_KEY = "9ff6b051db4649b7a180ab750b562780"

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)
    covid =  get_covidNews(NEWS_API_KEY)

    return render_template("home.html", weather=weather, covid=covid)

@app.route("/news")
def news():
    news = request.args.get('search_news')
    if not news:
        news = 'covid'
    search = search_news(news, NEWS_API_KEY)

    return render_template("news.html", search=search)

@app.route('/about')
def about():
   return render_template('about.html')

def search_news(news,API_KEY):
    try:
        query = quote(news)
        url = NEWS_API_URL.format(news, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        search = parsed.get('articles')

        return search
    except:
        return 0

def get_covidNews(API_KEY):
    url = COVID_API_URL.format(API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    covid = list()

    for i in range(0,5):
        covid.append(parsed['articles'][i])
            
    return covid

def get_weather(city,API_KEY):
    try:
        query = quote(city)
        url = OPEN_WEATHER_URL.format(city, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        weather = None

        if parsed.get('weather'):

            temperature = parsed['main']['temp']
            description = parsed['weather'][0]['description']
            pressure = parsed['main']['pressure']
            humidity = parsed['main']['humidity']
            speed = parsed['wind']['speed']
            icon = parsed['weather'][0]['icon']
            city = parsed['name']
            country = parsed['sys']['country']

            weather = {'temperature': temperature,
                        'description': description,
                        'pressure' : pressure,
                        'humidity' :  humidity,
                        'speed' : speed,
                        'icon' : icon,
                        'city': city,
                        'country': country
                       }
        return weather
    except:
        return 0

app.env="development"
app.run(debug=True)