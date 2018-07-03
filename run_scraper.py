from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import json
import sys

#TODO: run node script and update firebase. also nest current data under "non deleon"

def scrape_non_deleon():
    NUM_PAGES_TO_SCRAPE = 7
    sv_open_house_map = {}
    for i in range(2, NUM_PAGES_TO_SCRAPE):
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
        # To limit number of houses to pull, set count
        # count = -1
        for house_info in sv_open_house_url_arr:
            # count += 1
            # if count < 2:
            #Scrape information from an individual listing
            house_url=house_info[0]
            house_key=house_info[1]
            r = requests.get(house_url)
            data = r.text
            soup = BeautifulSoup(data, "html.parser")
            house_map = {}
            house_map["Page"] = str(i)
            main_info_map = {"desc": ["div", "col-md-12 ihf-description"],
            "beds": ["div", "property-main-detail-item ihf-bedrooms"],
            "baths": ["div", "property-main-detail-item ihf-baths"],
            "sq ft": ["div", "property-main-detail-item ihf-square-feet"],
            "property type": ["div", "property-main-detail-item ihf-property-type"],
            "price": ["span", "ihf-for-sale-price"]
            }
            for info in main_info_map.keys():
                find_info = soup.find(main_info_map[info][0], {"class": main_info_map[info][1]}).contents
                if len(find_info) > 0:
                    house_map[info] = find_info[0]
                else:
                    house_map[info] = "NO " + info.upper()
            house_features = soup.findAll("div", {"class": "listing-info-item"})
            for feature in house_features:
                title = feature.contents[1].contents[0][:-1]
                value = feature.contents[2][1:]
                title = re.sub('[^0-9a-zA-Z]+', ' ', title)
                house_map[title] = value
            sv_open_house_map[house_key] = house_map
    print(json.dumps(sv_open_house_map))

def scrape_deleon():
    MAX_TABS = 20
    sv_homes_url = "https://deleonrealty.com/deleon-properties/status/"
    r  = requests.get(sv_homes_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    house_listings = soup.findAll("div", {"class": "av-inner-masonry-content-pos-content"})
    deleon_houses_url_arr = []
    deleon_houses_map = {}
    #Get urls of open house listings on this page
    for listing in house_listings:
        address = listing.find("h3", {"class": "av-masonry-entry-title entry-title"}).contents[0]
        subtitle = listing.find("div", {"class" : "av-masonry-entry-content entry-content"}).contents[0]
        url_address = re.sub('[^0-9a-zA-Z]+', '-', address)
        house_url = "https://deleonrealty.com/property/" + url_address
        deleon_houses_url_arr.append([house_url, url_address, subtitle])
    for house_info in deleon_houses_url_arr:
        house_map = {}
        house_url=house_info[0]
        house_key=house_info[1]
        house_subtitle=house_info[2]
        house_map["status or price"] = house_subtitle
        r = requests.get(house_url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        for i in range(1, MAX_TABS):
            potential_tab = soup.find("div", {"id": "tab-id-" + str(i) + "-container"})
            if potential_tab is None:
                break
            tab_title = soup.find("div", {"data-fake-id": "#tab-id-"+str(i)}).contents[0]
            children = potential_tab.find_all("p")
            children += potential_tab.find_all("li")
            child_contents = ""
            for child in children:
                if child.find("strong") is None and child.find("span") is None:
                    child_contents += " " + child.contents[0]
            house_map["desc:" + tab_title] = child_contents
        info_table = soup.find("table")
        if info_table is not None:
            table_rows = info_table.findAll("tr")
            for row in table_rows:
                row_heading = row.find("th").contents[0]
                row_content_soup = row.find("td")
                if row_content_soup.find("small") is not None:
                    #take content from within small tag
                    row_content = row_content_soup.find("small").contents[0]
                else:
                    row_content = row_content_soup.contents[0]
                #The data is NOT formatted the same way as in scrape_non_deleon.
                #i.e. "Listed at" vs "price", tabs vs. random house stats
                #Must clean after retrieving data
                house_map[row_heading] = row_content
        deleon_houses_map[house_key] = house_map
    print(json.dumps(deleon_houses_map))

def main():
    scrape_deleon()
if __name__ == '__main__':
    main()
