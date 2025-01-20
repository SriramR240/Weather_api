#import necessary libraries
import requests
import sys
import os
from dotenv import load_dotenv, find_dotenv
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
import csv
import redis

#load environment variables
load_dotenv(find_dotenv())
API_KEY = os.getenv('KEY')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

@on_exception(expo, RateLimitException, max_tries=8)
@limits(calls=15, period=900)
def call_api(weather_api_url):
    """
    Calls the WeatherApi , a max of 15 calls can be made in 15 minutes
    :param weather_api_url:
    :return: CSVReader of response
    """
    try:
        response = requests.request("GET", weather_api_url)
    except:
        print("Error connecting to API")
        sys.exit()

    if response.status_code != 200:
        print('Unexpected Status code: ', response.status_code)
        sys.exit()

    print("Data Retrieved from Api")
    try:
        r.set(city, response.text)
    except:
        print("Cannot cache to redis.Connection failed")

    csvtext = csv.reader(response.text.splitlines(), delimiter=',', quotechar='"')
    
    return csvtext
    


if __name__ == '__main__':

    city = input("Enter a city to get weather data for:" )
    cached_response = None

    try:
        r = redis.Redis(host=HOST, port=PORT, decode_responses=True)
        print("Connection to redis success")
        cached_response = r.get(city)
    except:
        print("Connection to Redis Failed")

    if not cached_response:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=us&include=days&key={API_KEY}&contentType=csv"
        print("Calling Weather API")
        CSVText = call_api(url)
    else:
        CSVText = csv.reader(cached_response.splitlines(), delimiter=',', quotechar='"')
        print("Cached data Retrieved")

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(CSVText)
        print("Data written to file")