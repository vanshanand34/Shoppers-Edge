def myoutput(search_text):
    output=[{
        "name":"boat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatch",
        "price":"2817",
        "rating":"5",
        "link":"www.amazon.in/trimmerboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatchboat smartwatch",
        "site":"amazon"
    },
    {
        "name":"boat shhkamartwatch",
        "price":"93289",
        "rating":"5",
        "link":"www.amazon.in/trimmer",
        "site":"amazon"
    },
    {
        "name":"boat kjhadkh smartwatch",
        "price":"2200",
        "rating":"5",
        "link":"www.amazon.in/trimmer",
        "site":"amazon"
    },
    {
        "name":"boat triommer",
        "price":"28837",
        "rating":"5",
        "link":"www.amazon.in/trimmer",
        "site":"amazon"
    }]
    return output




# #Price Extraction function for shopper's edge -> tushar anand


# #Importing necessary Modules

# from playwright.sync_api import sync_playwright
# from selectolax.parser import HTMLParser
# import pandas as pd
# import time
# from bs4 import BeautifulSoup

# #extracting html source using plawright

# def get_html(page,asin,website):

#     searchtext = asin.replace(' ','%20')

#     if website == 'flipkart':
#         flp_str1="https://www.flipkart.com/search?q="
#         flp_str2="&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY"
#         url = flp_str1 + searchtext + flp_str2   

#     elif website == "amazon":
#         amz_str1="https://www.amazon.in/s?k="
#         amz_str2="&ref=nb_sb_noss_2"
#         url = amz_str1 + searchtext + amz_str2

#     elif website =='jiomart':
#         jio_str1 = "https://www.jiomart.com/search/"
#         url = jio_str1 + searchtext

#     page.goto(url)
#     time.sleep(2)
#     soup = BeautifulSoup(page.content(), "html.parser")
#     return soup

# #cleaning and parsing the html

# def parse_html(soup,website):

#     result=[]

#     if website=='jiomart':

#         for link in soup.find_all("a",class_="plp-card-wrapper plp_product_list"):

#             try:

#                 #gathering the required data from webpage

#                 temp = {'site':'jiomart'}
#                 temp['link'] = "https://www.jiomart.com" + link.get('href')
#                 card = link.find("div",class_="plp-card-container")
#                 temp['name' ]= card.find("div",class_="plp-card-details-name").text
#                 temp['price'] = card.find("div",class_="plp-card-details-price").find("span").text
#                 temp['price'] = temp['price'].replace('₹','')
#                 temp['price'] = temp['price'].replace(',','')
#                 temp['price'] = 'Rs' + ' ' + temp['price']
#                 temp['rating'] = "Unavailable"
#                 result.append(temp)

#             except:
#                 pass

#     elif website =='amazon':

#         div_element = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
#         for div in div_element:

#             if 'Adholder' in div.get('class'):
#                 pass
#             else:
#                 try:

#                     #gathering the required data from webpage

#                     temp = {'site':'amazon'}
#                     temp['price'] = div.find("span",class_="a-price-whole").text
#                     temp['price'] = temp['price'].replace('₹','')
#                     temp['price'] = temp['price'].replace(',','')
#                     temp['price'] = 'Rs' + ' ' + temp['price']
#                     temp['name'] = div.find("h2").text
#                     temp['link'] = "https://www.amazon.in" + div.find("h2").find("a").get("href")
#                     temp['rating'] = div.find("i",class_="a-icon-star-small" ).find("span").text
#                     print(temp)
#                     result.append(temp)
#                 except:
#                     pass

        


#     return result


# #gathering all the details and making a final function
# def clean_data(fetched_data):
#     final_data=list()
#     for i in range(0,len(fetched_data)):
#         temp={
#             "name":fetched_data["name"][i],
#             "price":fetched_data["price"][i],
#             "rating":fetched_data["rating"][i],
#             "link":fetched_data["link"][i],
#             "site":fetched_data["site"][i]
#         }  
#         final_data.append(temp)
#     return final_data


# def myoutput(search_text):

#     search_text = search_text.replace(" ","%20")
#     asin = search_text
#     pw = sync_playwright().start()
#     browser = pw.chromium.launch()
#     page = browser.new_page()
#     supported_sites = ['jiomart','amazon']
#     results=[]
#     for site in supported_sites:
#         try:
#             html = get_html(page,asin,site)
#             results.extend(parse_html(html,site))
#         except:
#             pass
#     fetched_data=pd.DataFrame(results)
#     cleaned_data = clean_data(fetched_data)
#     return cleaned_data
