import requests
from bs4 import BeautifulSoup
import pandas as pd

# This program prints Florida weather foreCast from a static page
# Code was adapted from "https://www.dataquest.io/blog/web-scraping-tutorial-python/"


# Get Florida weather page
page = requests.get("http://forecast.weather.gov/MapClick.php?lat=28.566&lon=-81.6886")
# print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

# seven_day = soup.find(id="seven-day-forecast")
foreCastBody = soup.find('div', id="seven-day-forecast-body")

periodList = [w.get_text() for w in foreCastBody.select(".tombstone-container .period-name")]
descList = [w.get_text() for w in foreCastBody.select(".tombstone-container .short-desc")]
tempList = [w.get_text() for w in foreCastBody.select(".tombstone-container .temp")]
detailsList = [w["title"] for w in foreCastBody.select(".tombstone-container .forecast-icon")]
# periodList = [w.select(".period-name")[0].get_text() for w in weatherList]
# descList = [w.select(".short-desc")[0].get_text() for w in weatherList]
# tempList = [w.select(".temp")[0].get_text() for w in weatherList]

weather = pd.DataFrame({
    "period": periodList,
    "desc": descList,
    "temp": tempList,
    "details": detailsList
})

tempNums = weather["temp"].str.extract("(?P<temp_nums>\d+)", expand=False)

weather["tempNums"] = tempNums.astype("int")

# print(weather["tempNums"].mean())

isnight = weather["temp"].str.contains("Low")
weather["isnight"] = isnight
print(weather[isnight])
