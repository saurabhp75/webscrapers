import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# This program prints the Delhi weather forecast.
# Headless chrome & Selenium is used to get data from dynamic page

# body > div > div:nth-child(7) > div.col-7.city_right_side

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


# Run browser in headless mode
browser = webdriver.Chrome(chrome_options=chrome_options,
                           executable_path='C:\\Users\\saura\\Downloads\\chromedriver_win32\\chromedriver.exe')
# Run browser with GUI
# browser = webdriver.Chrome('C:\\Users\\saura\\Downloads\\chromedriver_win32\\chromedriver.exe')

# Get Delhi weather page
# Get Delhi weather page
browser.get('https://worldweather.wmo.int/en/city.html?cityId=224')
browser.implicitly_wait(5)  # seconds

# capture the screen
# browser.get_screenshot_as_file("capture.png")

contentHtml = browser.find_element_by_class_name("col-7")
# print(type(contentHtml)) # <class 'selenium.webdriver.remote.webelement.WebElement'>
contentToParse = contentHtml.get_attribute("innerHTML")
# print(type(contentToParse)) # <class 'str'>
soup = BeautifulSoup(contentToParse, 'html.parser')

dateList = [elem1.get_text() for elem1 in soup.select(".city_fc_date")]
minTempList = [elem1.get_text() for elem1 in soup.select(".min_temp_box")]
maxTempList = [elem2.get_text() for elem2 in soup.select(".max_temp_icon")]
descList = [elem3.get_text() for elem3 in soup.select(".city_fc_desc")]

weather = pd.DataFrame({
    "MinTemp": minTempList,
    "MaxTemp": maxTempList,
    "Desc": descList,
    "Date": dateList
})
# print(weather)
mxNums = weather["MaxTemp"].str.extract("(?P<mxTemp>\d+)", expand=False)
mnNums = weather["MinTemp"].str.extract("(?P<mnTemp>\d+)", expand=False)

# print(mxNums)
weather["mxTemp"] = mxNums.astype('int')
weather["mnTemp"] = mnNums.astype('int')
print(weather)

# browser.wait(5)
# browser.close()
