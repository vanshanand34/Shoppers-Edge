import threading
from celery import shared_task
import playwright
from bs4 import BeautifulSoup
import pandas as pd

# Scrape function for a single website
def scrape_site(text, website):

    searchtext = text.replace(' ', '%20')

    url_mappings = {
        'flipkart': f"https://www.flipkart.com/search?q={searchtext}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY",
        'amazon': f"https://www.amazon.in/s?k={searchtext}&ref=nb_sb_noss_2",
        'jiomart': f"https://www.jiomart.com/search/{searchtext}",
    }

    try:
        # Playwright interaction
        with playwright.chromium.launch() as pw:
            browser = pw.new_context()
            page = browser.new_page()
            page.goto(url_mappings[website])

            # Page scraping using BeautifulSoup
            soup = BeautifulSoup(page.content(), "html.parser")
            return parse_html(soup, website)

    except Exception as e:
        print(f"Error scraping {website}: {e}")
        return []

# Parse and extract data
def parse_html(soup, website):

    result = []

    if website == 'jiomart':
        # Extract data specific to JioMart
        for link in soup.find_all("a", class_="plp-card-wrapper plp_product_list"):
            try:
                temp = {'site': 'jiomart'}
                temp['link'] = "https://www.jiomart.com" + link.get('href')
                card = link.find("div", class_="plp-card-container")
                temp['name'] = card.find("div", class_="plp-card-details-name").text
                temp['price'] = card.find("div", class_="plp-card-details-price").find("span").text
                temp['price'] = temp['price'].replace('₹', '')
                temp['price'] = temp['price'].replace(',', '')
                temp['price'] = 'Rs ' + temp['price']
                temp['rating'] = "Unavailable"
                result.append(temp)
            except:
                pass

    elif website == 'amazon':
        # Extract data specific to Amazon
        div_element = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
        for div in div_element:
            if 'Adholder' in div.get('class'):
                pass
            else:
                try:
                    temp = {'site': 'amazon'}
                    temp['price'] = div.find("span", class_="a-price-whole").text
                    temp['price'] = temp['price'].replace('₹', '')
                    temp['price'] = temp['price'].replace(',', '')
                    temp['price'] = 'Rs ' + temp['price']
                    temp['name'] = div.find("h2").text
                    temp['link'] = "https://www.amazon.in" + div.find("h2").find("a").get("href")
                    temp['rating'] = div.find("i", class_="a-icon-star-small").find("span").text
                    result.append(temp)
                except:
                    pass

    elif website == 'flipkart':
        # Extract data specific to Flipkart
        div_elements = soup.find_all("div", {"data-id": True})
        for div in div_elements:
            data_text = div.text
            if 'Sponsored' in data_text:
                pass
            else:
                try:
                    temp = {'site': 'flipkart'}
                    temp['price'] = div.find("div", class_="_30jeq3").text
                    temp['price'] = temp['price'].replace('₹', '')
                    temp['price'] = temp['price'].replace(',', '')
                    temp['price'] = temp['price']
                    temp['name'] = div.find_all("a")[1].text
                    temp['link'] = "https://www.flipkart.com" + div.find_all("a")[0].get("href")
                    temp['rating'] = 0
                    try:
                        temp['rating'] = div.find("div", class_="_3LWZlK").text
                        temp['name'] = temp['name'] + " Quantity : " + div.find("div", class_="_3Djpdu").text
                    except:
                        pass
                    result.append(temp)
                except:
                    pass

    return result

# Clean and format data
def clean_data(fetched_data):
    final_data = []
    for i in range(0, len(fetched_data)):
        temp = {
            "name": fetched_data["name"][i],
            "price": fetched_data["price"][i],
            "rating": fetched_data["rating"][i],
            "link": fetched_data["link"][i],
            "site": fetched_data["site"][i],
        }
        final_data.append(temp)
    return final_data

@shared_task
def myoutput(search_text):
    search_text = search_text.replace(" ", "%20")
    threads = []
    supported_sites = ['jiomart']
    results = []

    # Create threads for scraping each website
    for site in supported_sites:
        thread = threading.Thread(target=scrape_site, args=(search_text, site))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    results = [thread.result() for thread in threads]


    # Convert to DataFrame and clean data
    fetched_data = pd.DataFrame(results)
    cleaned_data = clean_data(fetched_data)

    return cleaned_data
myoutput('trimmer')