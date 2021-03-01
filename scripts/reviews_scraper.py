from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/cha/Downloads/chromedriver_2", chrome_options=options)


def get_top3_reviews(artist, album):
    #build URL
    artist_transformed = artist.replace(" ", "+")
    album_transformed = album.replace(" ", "+")
    url = f"https://www.allmusic.com/search/albums/{artist_transformed}+{album_transformed}"

    #retrieve webpage content using Selenium
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features="lxml")

    #locate first album and prepare URL to user reviews
    url_2 = soup.find("div", class_="title").find("a")['href']
    url_reviews = f"{url_2}/user-reviews"

    #retrieve user reviews page
    driver.get(url_reviews)
    page_source_2 = driver.page_source
    soup = BeautifulSoup(page_source_2, features="lxml")

    #extract reviews into a list
    reviews = []
    for review in soup.find_all("div", class_="user_review"):
        review_div = review.find("div", class_="middle")
        reviews.append(review_div.text)

    #display top 3 reviews
    return reviews[:2]
