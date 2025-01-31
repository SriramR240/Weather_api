# Weather API Data Fetcher

This Python script retrieves weather data from the Visual Crossing Weather API and caches responses using Redis to optimize API calls. The data is saved in a CSV file for easy access.

## Features
- Fetches weather data for a user-specified city using the Visual Crossing Weather API.
- Implements rate limiting to stay within API request limits (max **15 calls per 15 minutes**).
- Uses Redis caching to store and retrieve previously fetched weather data, reducing API calls.
- Saves the retrieved weather data into a CSV file (`output.csv`).

## Prerequisites
Ensure you have the following installed:
- **Python 3.7+**
- **Redis** (running locally or accessible remotely)
- **Visual Crossing Weather API Key** (Get one from [Visual Crossing Weather](https://www.visualcrossing.com/weather-api))

project url : https://roadmap.sh/projects/weather-api-wrapper-service
