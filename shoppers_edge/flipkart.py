

#Importing necessary Modules
import asyncio
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
import pandas as pd
import time
from bs4 import BeautifulSoup

#extracting html source using plawright

async def get_html(page,asin,website):

    searchtext = asin.replace(' ','%20')

    if website == 'flipkart':
        flp_str1="https://www.flipkart.com/search?q="
        flp_str2="&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY"
        url = flp_str1 + searchtext + flp_str2   

    elif website == "amazon":
        amz_str1="https://www.amazon.in/s?k="
        amz_str2="&ref=nb_sb_noss_2"
        url = amz_str1 + searchtext + amz_str2

    elif website =='jiomart':
        jio_str1 = "https://www.jiomart.com/search/"
        url = jio_str1 + searchtext

    await page.goto(url)
    time.sleep(2)
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    return soup

#cleaning and parsing the html

def parse_html(soup,website):

    result=[]

    if website=='jiomart':
        counter=0
        for link in soup.find_all("a",class_="plp-card-wrapper plp_product_list"):
            if counter > 10:
                break
            counter+=1
            try:

                #gathering the required data from webpage

                temp = {'site':'jiomart'}
                temp['link'] = "https://www.jiomart.com" + link.get('href')
                card = link.find("div",class_="plp-card-container")
                temp['name' ]= card.find("div",class_="plp-card-details-name").text
                temp['price'] = card.find("div",class_="plp-card-details-price").find("span").text
                temp['price'] = temp['price'].replace('₹','')
                temp['price'] = temp['price'].replace(',','')
                temp['price'] = temp['price'].replace('Rs','')
                temp['rating'] = "-"
                result.append(temp)

            except:
                pass

    elif website =='amazon':

        div_element = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
        counter=0
        for div in div_element:
            if counter > 10:
                break
            if 'Adholder' in div.get('class'):
                pass
            else:
                counter+=1
                try:

                    #gathering the required data from webpage

                    temp = {'site':'amazon'}
                    temp['price'] = div.find("span",class_="a-price-whole").text
                    temp['price'] = temp['price'].replace('₹','')
                    temp['price'] = temp['price'].replace(',','')
                    temp['price'] = temp['price'].replace('Rs','')
                    temp['name'] = div.find("h2").text
                    temp['link'] = "https://www.amazon.in" + div.find("h2").find("a").get("href")
                    temp['rating'] = div.find("i",class_="a-icon-star-small" ).find("span").text
                    result.append(temp)
                except:
                    pass

    elif website=='flipkart':
            div_elements = soup.find_all("div", {"data-id": True})
            # Access individual div elements
            counter=0
            for div in div_elements:
                if counter > 10:
                    break
                data_text = div.text
                if 'Sponsored' in data_text:
                    pass
                else:
                    counter+=1
                    try:
                        temp = {'site':'flipkart'}
                        temp['price'] = div.find("div",class_="_30jeq3").text
                        temp['price'] = temp['price'].replace('₹','')
                        temp['price'] = temp['price'].replace(',','')
                        temp['price'] = temp['price'].replace('Rs','')
                        temp['name'] = div.find_all("a")[1].text
                        temp['link'] = "https://www.flipkart.com" + div.find_all("a")[0].get("href")
                        temp['rating'] = 0
                        try:
                            temp['rating'] = div.find("div",class_="_3LWZlK").text
                            temp['name'] = temp['name'] + " Quantity : "  + div.find("div",class_="_3Djpdu").text
                        except:
                            pass
                        result.append(temp)
                    except:
                        pass
    return result


#gathering all the details and making a final function
def clean_data(fetched_data):
    final_data=list()
    for i in range(0,len(fetched_data)):
        temp={
            "name":fetched_data["name"][i],
            "price":int(fetched_data["price"][i]),
            "rating":fetched_data["rating"][i],
            "link":fetched_data["link"][i],
            "site":fetched_data["site"][i]
        }  
        final_data.append(temp)
    return final_data

async def runn(asin,pw):
        browser = await pw.chromium.launch()
        page1 = await browser.new_page()
        page2 = await browser.new_page()
        page3 = await browser.new_page()
        pages = [page1,page2,page3]
        supported_sites = ['flipkart','amazon','jiomart']
        results=[]
        i=0
        for site in supported_sites:
            try:
                html = await get_html(pages[i],asin,site)
                print(site)
                results.extend(parse_html(html,site))
            except:
                pass
            i+=1
        await browser.close()
        fetched_data=pd.DataFrame(results)
        cleaned_data = clean_data(fetched_data)
        return cleaned_data

async def myoutput(search_text):
    search_text = search_text.replace(" ","%20")
    asin = search_text
    async with async_playwright() as pw:
        return await runn(asin,pw)
