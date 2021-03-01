from bs4 import BeautifulSoup
import requests

def get_price(artist, album):
    # buid URL
    artist_transformed = artist.replace(" ", "+")
    album_transformed = album.replace(" ", "+")
    url = f"https://www.discogs.com/search/?q={artist_transformed}+{album_transformed}&type=all&format_exact=Vinyl"

    # retrieve master_id
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    card = soup.find('div', attrs={"class":["shortcut_navigable"]})
    master_id = card.attrs["data-master-id"]

    # dynamically update the result URL
    link = f"https://www.discogs.com/sell/list?sort=price%2Casc&limit=25&master_id={master_id}&ev=mb&format=Vinyl&currency=EUR"
    response_3 = requests.get(link)
    soup = BeautifulSoup(response_3.content, "html.parser")

    # retrieve all prices
    items = []
    for price in soup.find_all("span", class_="converted_price"):
        price_stripped = float(price.text.strip('about').strip('total').strip(' ')[1:])
        items.append(price_stripped)

    #find_minimum price
    min_price = min(items)

    return min_price
