import requests
import sys
import os
from dotenv import load_dotenv, find_dotenv
import csv
import redis

load_dotenv(find_dotenv())

API_KEY = os.getenv('KEY')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == '__main__':

    city = input("Enter a city to get weather data for:" )

    r = redis.Redis(host=HOST, port=PORT, decode_responses=True)

    cached_response = r.get(city)
    print(cached_response)
    if not cached_response:

        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=us&include=days&key={API_KEY}&contentType=csv"

        response = requests.request("GET",url)

        if response.status_code != 200:
            print('Unexpected Status code: ', response.status_code)
            sys.exit()

        print("Data Retrieved")
        r.set(city, response.text)
        CSVText = csv.reader(response.text.splitlines(), delimiter=',', quotechar='"')

    else:
        CSVText = csv.reader(cached_response.splitlines(), delimiter=',', quotechar='"')
        print("Cached data Retrieved")

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(CSVText)