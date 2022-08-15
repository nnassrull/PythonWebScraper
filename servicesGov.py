import requests
import re
from bs4 import BeautifulSoup
from csv import writer

url = "https://services.india.gov.in/service/ministry_services?cmd_id=1897&ln=en"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html5lib')

services = soup.find('nav', class_='naver').find('ul').find_all('li')

with open('services.csv', 'w', newline='', encoding='utf8') as f:
    thewriter = writer(f)
    header = ['Ministry Name', "Number of Services", "Associated Link"]
    thewriter.writerow(header)

    for service in services:
        ministry = service.text
        anchor = service.find('a')
        servicesNumber = service.text
        pattern = r'[0-9]'
        ministry = re.sub(pattern, '', ministry)
        ministry = re.sub(r"[\([{})\]]", "", ministry)
        ministry = ministry.strip()
        servicesNumber = re.sub("\D", "", servicesNumber)
        Link = anchor['href'];
        Row = [ministry, servicesNumber, Link]
        thewriter.writerow(Row)
f.close()
