import requests
from bs4 import BeautifulSoup
from csv import writer
from csv import reader

def ratingCalc(x):
        if(x == 0):
            return 0
        elif (x > 0 and x <= 25):
            return 1
        elif (x > 25 and x <= 45):
            return 2
        elif (x > 45 and x <= 65):
            return 3
        elif (x > 65 and x <= 85):
            return 4
        elif (x > 85 and x <= 100):
            return 5
        else:
            return

urls = []            
url = 'https://services.india.gov.in/service/ministry_services?ln=en&cmd_id=1126'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html5lib')
ministries = soup.find('nav', class_='naver').find('ul').find_all('li')
for ministry in ministries:
    anchor = ministry.find('a')
    Link = anchor['href']
    urls += [Link]


with open('servicesDesc.csv', 'w', newline='', encoding='utf8') as f:
    thewriter = writer(f)
    header = ['Ministry', 'Type of Service', 'Service Status', 'Service Rating', 'Service Description', 'Linked Site', 'Registration Required']
    thewriter.writerow(header)

for url in urls: 
    for i in range(12):
        if (i != 0):
            url = url + '&page_no=' + str(i+1)
        page = requests.get(url)
        if(page.content):
            soup = BeautifulSoup(page.content, 'html5lib')
            services = soup.find_all('div', class_='edu-lern-con')
            category = soup.find('div', class_='title-left').find('h2')
            categoryText = category.text.strip()
            with open('servicesDesc.csv', 'a', newline='', encoding='utf8') as f:
                thewriter = writer(f)
                for service in services:
                    anchor = service.find('a', class_='ext-link')
                    status = service.find('li', class_='status_icon')
                    rating = service.find('span', class_='star_rating_stars')
                    ratingNo = rating['style'].lstrip('width:').rstrip('%;')
                    ratingNo = int(ratingNo)
                    ratingFinal = ratingCalc(ratingNo)
                    desc = service.find('p')
                    desc = desc.text.strip()
                    Link = anchor['href']
                    RegReq = 'N'
                    if(service.find('li', class_='tag_light')):
                        RegReq = 'Y'
                    Row = [category.text.strip(), anchor.text.strip(), status.text.strip(), ratingFinal, desc, Link.strip(), RegReq]
                    thewriter.writerow(Row)
        else:
            continue
f.close();

# RegReqN = []

# with open('servicesDesc.csv', 'r', encoding='utf8') as f:
#     thereader = reader(f)
#     next(thereader)
#     for line in thereader:
#         if(line[5] == 'N'):
#             RegReqN += line

# urls = [] 

# for i in range(len(RegReqN)):
#     if(RegReqN[i][4].startswith("https")):
#         urls += RegReqN[i][4]

# for url in urls:
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html5lib')
#     Links = soup.find_all('a')
#     NumberOfLinks = Links.len()


    
