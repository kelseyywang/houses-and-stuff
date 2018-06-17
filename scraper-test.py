#For testing part of run_scraper.py
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import json

#On 6/4/2018, this should be 7 when you want all listings.
#TODO: check when pages get repetitive = end of new pages
NUM_PAGES_TO_SCRAPE = 1

sv_open_house_map = {}
#PART 1: GET DATA FROM OPEN LISTINGS
for i in range(NUM_PAGES_TO_SCRAPE):
    sv_homes_url = "https://deleonrealty.com/listing-report/Silicon-Valley/467825/?pg=" + str(i)
    r  = requests.get(sv_homes_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    house_listings = soup.findAll("div", {"class": "ihf-grid-result-container well"})
    sv_open_house_url_arr = []
    #Get urls of open house listings on this page
    for listing in house_listings:
        address_arr = listing.find("span", {"class": "ihf-grid-result-address"}).contents
        address = address_arr[0] + address_arr[2]
        url_address = re.sub('[^0-9a-zA-Z]+', '-', address)
        id_arr = listing.find("div", {"class": "ihf-grid-result-mlsnum-proptype"}).contents
        end_index = id_arr[0].find('|') - 1
        url_id = id_arr[0][1:end_index]
        house_url = "https://deleonrealty.com/homes-for-sale-details/" + url_address[1:-1] + "/" + url_id + "/190/"
        sv_open_house_url_arr.append([house_url, url_address[1:-1]])

    #To access all urls, use below: for house_url in sv_open_house_url_arr:
    count = -1
    for house_info in sv_open_house_url_arr:
        count += 1
        if count < 5:
            #Scrape information from an individual listing
            house_url=house_info[0]
            house_key=house_info[1]
            r  = requests.get(house_url)
            data = r.text
            soup = BeautifulSoup(data, "html.parser")
            house_map = {}
            house_map["Page"] = str(i)
            potential_desc = soup.find("div", {"class": "col-md-12 ihf-description"}).contents
            if len(potential_desc) > 0:
                house_map["desc"] = potential_desc[0]
            else:
                house_map["desc"] = "NO DESCRIPTION"
            house_features = soup.findAll("div", {"class": "listing-info-item"})
            for feature in house_features:
                title = feature.contents[1].contents[0][:-1]
                value = feature.contents[2][1:]
                title = re.sub('[^0-9a-zA-Z]+', '*', title)
                house_map[title] = value
            sv_open_house_map[house_key] = house_map
#Debug: print map
# print(json.dumps(sv_open_house_map, indent=4, sort_keys=True))
