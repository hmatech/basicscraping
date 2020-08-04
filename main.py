import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep

print('+'*30)
print('+Basic web scraping, searching for product')
print('+Target: NAMA - Indonesia')
print('+Created by Habibie Muhammad A')
print('+'*30)
url = None
req = None
baseurl = 'https://www.nama-indonesia.com/'
try:
    keyword = input('Masukkan kata kunci pencarian: ')
    url = f'https://www.nama-indonesia.com/search?q={keyword}*'
    print('Url: ', url)
    print('Requesting...')
    req = rq.get(url)
    if req.status_code == 200:
        print('Request succesfull, status code: ', req.status_code)
        sleep(2)
    else:
        print('Oops! An error occured, status code: ', req.status_code)
except Exception as e:
    print('Oops! Something error: ', e)

print(f"=========SITE: {url}==========")
sleep(2)
sup = BeautifulSoup(req.content, "html.parser")
print("Site title: ", baseurl)
print("Fetching products...")
productresult = sup.find_all('div', class_='search-result__description')
print(f"Found {len(productresult)} products")
sleep(5)
count = 0
for pr in productresult:
    title = pr.find('a')
    descrip = pr.find('p')
    link1 = pr.find('a')['href']
    descript = descrip.text.strip()
    full_link = urljoin(baseurl, link1)
    print('='*25, f'Product #{count+1}', '='*25)
    print(f"Product's Title: {title.get('title')}")
    print(f"Product's description: \n\t{descript}")
    print(f"Link: {full_link}")
    print('='*63, '\n')
    count += 1

choice = input(f'Do you want to get all links from {baseurl}?(Y/N): ')
if choice == 'Y' or choice == 'y':
    print("Searching all links on the site...")
    search_link = sup.find_all('a')
    print(f"found {len(search_link)} link(+s)")
    for link1 in search_link:
        linkreal = link1.get('href')
        print(linkreal)
elif choice == 'N' or choice == 'n':
    print('Okay. No problem')
else:
    print("Sorry, that choice isn't exist!")
