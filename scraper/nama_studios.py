import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
from tqdm import tqdm


baseurl = 'https://www.nama-indonesia.com'


def req_url():
    try:
        keyword = input('Enter a keyword: ').replace(' ', '%20')
        url = f'https://www.nama-indonesia.com/search?q={keyword}*'
        print('Url: ', url)
        print('Requesting...')
        req = rq.get(url)
        base = rq.get(baseurl)
        title = BeautifulSoup(base.content, 'lxml')
        if req.status_code == 200:
            print('Request succesfull, status code: ', req.status_code)
            print('Site Title: ', title.title.string)
            sleep(1)
            return req, url
        else:
            print('Oops! An error occured, status code: ', req.status_code)
    except Exception as e:
        print('Oops! Something error: ', e)


product_title = []
product_desc = []
product_link = []


def search_product():
    req, url = req_url()
    print(f"=========SITE: {url}==========")
    sleep(1)
    sup = BeautifulSoup(req.content, 'lxml')
    print("Fetching products...")
    productresult = sup.find_all('div', class_='search-result__description')
    print(f"Found {len(productresult)} products")
    progres = tqdm(productresult)
    sleep(1)
    for pr in progres:
        title = pr.find('a')
        descrip = pr.find('p')
        link1 = pr.find('a')['href']
        descript = descrip.text.strip()
        full_link = urljoin(baseurl, link1)
        product_title.append(title.get('title'))
        product_desc.append(descript.replace('\n', ' '))
        product_link.append(full_link)
        progres.set_description('Collecting data')
        sleep(0.5)
    print('==Data collecting is done==')
    while True:
        choice = input('Would you like to print the data? (Y/N): ')
        if choice == 'Y' or choice == 'y':
            print_product()
            break
        elif choice == 'N' or choice == 'n':
            print('Okay. No problem')
            break
        else:
            print("Sorry, that choice isn't exist!")
            continue


def print_product():
    count = 0
    for title, desc, link in zip(product_title, product_desc, product_link):
        print('=' * 25, f'Product #{count + 1}', '=' * 25)
        print(f"Product's Title: {title}")
        print(f"Product's description: \n\t{desc}")
        print(f"Link: {link}")
        print('=' * 63, '\n')
        sleep(0.5)
        count += 1


link_collective = []


def get_all_link():
    choice = input(f'Do you want to get all links from {baseurl}?(Y/N): ')
    if choice == 'Y' or choice == 'y':
        req1 = rq.get(baseurl)
        sup1 = BeautifulSoup(req1.content, 'lxml')
        print("Searching all links on the site...")
        search_link = sup1.find_all("a")
        print(f"found {len(search_link)} link(+s)")
        progressed = tqdm(search_link, desc='Collecting link')
        for link1 in progressed:
            linkreal = link1.get('href')
            if linkreal is not None:
                splitlink = linkreal.split('/')
                withous_https = 'www.nama-indonesia.com'
                if withous_https in splitlink:
                    link_collective.append(linkreal)
                else:
                    link_collective.append(baseurl + linkreal)
            else:
                pass
            sleep(0.1)
        print('==Data collecting is done==')
    elif choice == 'N' or choice == 'n':
        print('Okay. No problem')
    else:
        print("Sorry, that choice isn't exist!")
