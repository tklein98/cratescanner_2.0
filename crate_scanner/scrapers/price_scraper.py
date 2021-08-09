def get_price(artist, album):
    # build URL
    artist_transformed = artist.replace(" ", "+")
    album_transformed = album.replace(" ", "+")


    # retrieve master_id using Discogs API
    url = f"https://api.discogs.com/database/search?release_title={album_transformed}&artist={artist_transformed}&format=Vinyl&token=JROUhijcLnDuKfcxtqmMTqlDcJpuBybBQWPTdxyJ"
    # print(url)
    response = requests.get(url)
    master_url = response.json()['results'][0]['master_url']
    master_url_response = requests.get(master_url)
    main_release_url = master_url_response.json()["main_release_url"]
    main_release_url_response = requests.get(main_release_url)
    master_id = main_release_url_response.json()['master_id']
    real_master_url = main_release_url_response.json()['master_url']
    real_master_url_response = requests.get(real_master_url)

    lowest_price = real_master_url_response.json()['lowest_price']
    link = f"https://www.discogs.com/sell/list?master_id={master_id}&format=Vinyl"


    response = requests.get(link)
    soup = BeautifulSoup(response.text, features="lxml")
    soup.find_all('td', class_="item_description")

    # listings = soup.find_all("span", class_="converted_price")
    listings = soup.find_all("tr", class_="shortcut_navigable") 
        
    # # retrieve all total prices
    items = []
    for listing in listings:
        if listing.find("span", class_="converted_price"):
            price = listing.find("span", class_="converted_price")
            price_stripped = float(price.text.strip('about').strip('total').strip(' ').replace('€', '').replace('$', ''))
            items.append(price_stripped)

    if items == []:
        print("no price found", "no price found")

    # find_minimum price
    min_price = min(items)
    min_price_index = items.index(min_price)

    all_urls = []
    for listing in listings:
        if listing.find("span", class_="converted_price"):
            tag = listing.find("a")
            url = tag['href']
            all_urls.append(url)

    url_min_price = f"https://www.discogs.com/{all_urls[min_price_index]}"

    return [url_min_price, min_price]
