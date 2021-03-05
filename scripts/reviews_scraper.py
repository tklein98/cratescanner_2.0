from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from bs4 import BeautifulSoup
import os

GOOGLE_CHROME_BIN = os.environ['GOOGLE_CHROME_BIN']
CHROME_DRIVER = os.environ['CHROME_DRIVER']

options = Options()
options.binary_location = GOOGLE_CHROME_BIN
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)

def get_top3_reviews(artist, album):
    #build URL
    artist_transformed = artist.replace(" ", "+")
    album_transformed = album.replace(" ", "+")
    url = f"https://www.allmusic.com/search/albums/{artist_transformed}+{album_transformed}"

    #retrieve webpage content using Selenium
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features="lxml")

    #locate correct album and prepare URL to user reviews
    albums = soup.find_all("li", class_="album")

    # keep only albums with the right artist
    artists = []
    for element in albums:
        a_list = []
        if element.find("div", class_="artist"):
            tag = element.find("div", class_="artist")
            if tag.find("a"):
                a_list.append(tag)

                for a in a_list:
                    tag = a.find("a")
                    if tag.text.lower() == artist:
                        artists.append(element)

    #keep only albums with the right album name, and retrieve url
    album_list = []
    for element in artists:
        tag = element.find("div", class_="title").find("a")
        if tag.text.lower() == album:
            album_list.append(tag['href'])
    url_2 = album_list[0]

    #build url to the reviews page, and retrieve page
    url_reviews = f"{url_2}/user-reviews"
    driver.get(url_reviews)
    page_source_2 = driver.page_source
    soup = BeautifulSoup(page_source_2, features="lxml")

    #extract reviews into a list
    reviews = []
    for review in soup.find_all("div", class_="user_review"):
        review_div = review.find("div", class_="middle")
        reviews.append(review_div.text)

    # display message if no reviews were found
    if reviews == []:
        return False

    #display top 3 reviews
    return reviews[:2]
