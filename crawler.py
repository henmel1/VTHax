import requests
import re
import ipwhois
import pprint
import socket
import plotly.express as px
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

# method to crawl google dork search and create list of resulting affected websites
mapList = []

def dorkSearch(google_dork_search_query):
    results = []
    try:
        dork_search_page = requests.get(google_dork_search_query)
    
        URL_PATTERN = r'/url\?q=([^&]+)&amp;'
        urls = re.findall(URL_PATTERN, str(dork_search_page.content))

        for url in urls:
            result_dictionary = {'Link': url}
            results.append(result_dictionary)

        del results[-1]
        del results[-1]

        for dict in results:
            try:
                domain_pattern = r"https?://(?:www\.)?([a-zA-Z0-9.-]+)"

                match = re.match(domain_pattern, list(dict.values())[0])
                if match:
                    domain = match.group(1)
                else:
                    print("No match found for:", list(dict.values())[0])

                ip = getIP(str(domain))
                dict['IP'] = ip
                whoIs(ip)
                summary = summarize("whoIs.txt")
                dict['Description'] = summary[0]
                mapList.append(summary[1])
            except:
                print("The IP address for " + domain + " could not be found.\n")
    except:
        return {'Name': "Invalid URL"}
    return results

# method to get ip address of given url
def getIP(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        return None

# method to do a whois search on the inputted affected website
def whoIs(ip_address):
    try:
        obj = ipwhois.IPWhois(ip_address)
        results = obj.lookup_rdap()

        whois_text = pprint.pformat(results)

        with open("whoIs.txt", "w", encoding="utf-8") as file:
            file.write(whois_text)

        return whois_text
    except Exception as e:
        return str(e)

# method to summarize the whoIs text document
def summarize(file_path):
    with open(file_path, 'r') as file:
        whois_text = file.read()

    try:
        # Define regex patterns to match specific fields
        asn_pattern = r"'asn':\s*'(\d+)'"
        asn_date_pattern = r"'asn_date':\s*'(\d{4}-\d{2}-\d{2})'"
        country_code_pattern = r"'asn_country_code':\s*'([A-Z]+)'"
        network_cidr_pattern = r"'asn_cidr':\s*'([^']+)'"
        ip_version_pattern = r"'ip_version':\s*'(\w+)'"
        phone_pattern = r"'phone':\s*\[{'type':\s*'voice',\s*'value':\s*'([\d\s+-]+)'\}]"
        address_pattern = r"'address':\s+\[{'type':\s+None,\s+'value':\s+'(.*?)'\s*}\s*],"
        
        # Extract information using regex
        asn_match = re.search(asn_pattern, whois_text)
        asn_date_match = re.search(asn_date_pattern, whois_text)
        country_code_match = re.search(country_code_pattern, whois_text)
        network_cidr_match = re.search(network_cidr_pattern, whois_text)
        ip_version_match = re.search(ip_version_pattern, whois_text)
        phone_match = re.search(phone_pattern, whois_text)
        address_match = re.search(address_pattern, whois_text, re.DOTALL)

        # Append the extracted information to the sentence string
        extracted_info_sentence = ""
        country_codes = []
        if asn_match:
            extracted_info_sentence += f"ASN: {asn_match.group(1)} | "
        if asn_date_match:
            extracted_info_sentence += f"ASN Date: {asn_date_match.group(1)} | "
        if country_code_match:
            extracted_info_sentence += f"Country Code: {country_code_match.group(1)} | "
            country_codes.append(country_code_match.group(1))
        if network_cidr_match:
            extracted_info_sentence += f"Network CIDR: {network_cidr_match.group(1)} | "
        if ip_version_match:
            extracted_info_sentence += f"IP Version: {ip_version_match.group(1)} | "
        if phone_match:
            extracted_info_sentence += f"Phone: {phone_match.group(1)} | "
        if address_match:
            address = address_match.group(1)
            formatted_address1 = address.replace(' ', '')
            formatted_address2 = formatted_address1.replace("'", "")
            formatted_address3 = formatted_address2.replace("\n", " ")
            formatted_address4 = formatted_address3.replace("\\n", " ")
            formatted_address5 = formatted_address4.replace(",", ", ")
            formatted_address6 = formatted_address5.replace("  ", " ")
            extracted_info_sentence += f"Address: {formatted_address6}"

        return extracted_info_sentence, country_codes

    except Exception as e:
        return str(e)
    
geolocator = Nominatim(user_agent="get_country_coordinates")
def get_country_coordinates(country_name):
    try:
        location = geolocator.geocode(country_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def map_gen():
    global mapList
    mapList = [r[0] for r in mapList]

    lat = []
    lon = []
    pop = []
    for country in mapList:
        try:
            lat.append(get_country_coordinates(country)[0])
            lon.append(get_country_coordinates(country)[1])
            pop.append(mapList.count(country))
        except:
            print("Latitude, longitude not valid")

    colors = []
    for i in range(len(mapList)):
        colors.append("Vulnerable Server Locations")

    print(mapList)
    print(lat)
    print(lon)
    print(pop)
    print(colors)

    data = np.array([mapList, lat, lon, colors, pop]).T
    df = pd.DataFrame(data, columns=['Map', 'Lat', 'Lon', 'Colors', 'Pop'])
    df['Lat'] = df['Lat'].astype(float)
    df['Lon'] = df['Lon'].astype(float)
    df['Pop'] = df['Pop'].astype(float)
    fig = px.scatter_geo(df, lat='Lat', lon='Lon', color="Colors", color_discrete_map={'Vulnerable Server Locations': 'red'}, title='Map of Vulnerable Servers Around the World', size="Pop")
    fig.show()