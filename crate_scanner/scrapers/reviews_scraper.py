from bs4 import BeautifulSoup
import requests


def get_top3_reviews(artist, album):

    artist_transformed = artist.replace(" ", "-")
    album_transformed = album.replace(" ", "-")
  
    #search for the artist first, and retrieve list of albums
    url = f"https://www.metacritic.com/person/{artist_transformed}"
    headermap = {"User-Agent": "Mac Firefox"}
    response = requests.get(url, headers = headermap)
    response.text

    soup = BeautifulSoup(response.text, "html.parser")
    albums = soup.find_all("td", class_="title brief_metascore")
    # extract albums into a list
    album_list = []
    for element in albums:
        tag = element.find("a")
        album_list.append(tag['href'])

    if album_list == []:
            return ['No reviews found.']


    # search for the provided album name in the results
    result = []
    for album in album_list:
        if album_transformed in album:
            result.append(album)
    
    if result == []:
            return ['No reviews found.']

    result_as_string = result[0]
    # build the album review url and put the results into a list
    url2 = f"https://www.metacritic.com{result_as_string}/user-reviews"
    print(url2)
    headermap = {"User-Agent": "Mac Firefox"}
    response = requests.get(url2, headers = headermap)
    response.text
    soup = BeautifulSoup(response.text, "html.parser")

    reviews = soup.find_all('span', class_="blurb blurb_expanded")

    reviews_list = []
    for review in reviews:
            review_div = review.get_text().strip()
            reviews_list.append(review_div)

            # display message if no reviews were found
    if reviews_list == []:
        return ["No reviews found."]

    return reviews_list[0:3]
            
       
