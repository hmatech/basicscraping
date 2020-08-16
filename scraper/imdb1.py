import requests as rq
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import time, sleep
import pandas as pd
from IPython.core.display import clear_output
from warnings import warn
from random import randint

baseurl = 'https://imdb.com/'


def req_url(url):
    try:
        header = {"Accept-Language": "en-US, en:q=0.5"}
        print('Url: ', url)
        print('Requesting...')
        req = rq.get(url, headers=header)
        if req.status_code == 200:
            print('Request succesfull, status code: ', req.status_code)
            return req
        else:
            print('Oops! An error occured, status code: ', req.status_code)
            return req
    except Exception as e:
        print('Oops! Something error: ', e)


# multiple pages list
pages_list = [i for i in range(0, 200, 50)]
years_list = [i for i in range(2010, 2011)]
request_total = len(pages_list) * len(years_list)
movie_total = request_total * 50

# movie data containers
mov_names = []
mov_year = []
mov_imdb = []
mov_metascore = []
mov_votes = []


def movie_scraper():
    # time start
    begin_time = time()
    request_count = 0

    # pages loop
    for year_url in years_list:
        for page in pages_list:
            url = f'https://www.imdb.com/search/title/?release_date={year_url}&sort=num_votes,desc&start={page + 1}'
            req = req_url(url)

            # request speed counter
            request_count += 1
            elapsed = time() - begin_time
            speed = request_count / elapsed
            print(f'Request #{request_count}, {speed:.3f} request/s')
            clear_output(wait=True)

            # warn if a request status code is not 200
            if req.status_code != 200:
                warn(f'Request #{request_count}, status code: {req.status_code}')

            # break the requests loop if exceed the limit
            if request_count > request_total:
                print("Request count exceed the expectation! Stopping...")
                break

            # parser
            soup = BeautifulSoup(req.content, 'lxml')
            contain_movies = soup.find_all('div', class_='lister-item mode-advanced')
            print(f'Found: {len(contain_movies)} movies')
            count = 0

            # movie data finders, and appenders
            for movie in tqdm(contain_movies, desc='Collecting data'):
                movie_metascore = movie.find('div', class_='ratings-metascore')
                if movie_metascore is not None:
                    print(f'-----Movie #{count + 1}-----')

                    # Name, year, episode, and episode year
                    movie_name = movie.h3.a.text
                    movie_year = movie.find('span', class_='lister-item-year').text
                    if movie_name not in mov_names:
                        mov_names.append(movie_name)
                        mov_year.append(movie_year)

                        # Rating
                        movie_imdb_rating = movie.find('div', class_='inline-block ratings-imdb-rating')['data-value']
                        mov_imdb.append(float(movie_imdb_rating))

                        # Metascore
                        movie_metascore = movie.find('span', class_='metascore').text
                        mov_metascore.append(int(movie_metascore))

                        # Vote
                        movie_vote = movie.find('span', attrs={'name': 'nv'})['data-value']
                        mov_votes.append(int(movie_vote))
                    else:
                        print("Same movie already stored: ", movie_name)
                        print("Skipping...")
                        pass
                    sleep(0.2)
                    count += 1
                    clear_output(wait=True)
            pageprint = 0
            if (page + 1) == 1:
                pageprint = 1
            elif (page + 1) == 51:
                pageprint = 2
            elif (page + 1) == 101:
                pageprint = 3
            elif (page + 1) == 151:
                pageprint = 4
            yearprint = year_url
            sleep(1)

            # some unimportant logic
            if len(years_list) != 1:
                if year_url != years_list[-1] and page != pages_list[-1]:
                    print(f'==Data collecting on year {yearprint} in page {pageprint} is done==')
                    print(f'Proceeding to scrape the next page...')
                    if page == pages_list[-1]:
                        yearprint += 1
                        pageprint = 0
                    print(f'Year: {yearprint}; Page: {pageprint + 1}')
                else:
                    print('All data have been succesfully collected and stored')
                    sleep(3)
                    print('Exiting...')
            else:
                if page != pages_list[-1]:
                    print(f'==Data collecting on year {yearprint} in page {pageprint} is done==')
                else:
                    print('All data have been succesfully collected and stored')
                    sleep(3)
                    print('Exiting...')

            sleep(randint(7, 13))


def append_data():
    global data_frame
    data_frame = pd.DataFrame(data={'movie': mov_names, 'year': mov_year, 'imdb': mov_imdb,
                                    'metascore': mov_metascore, 'votes': mov_votes},
                              columns=['movie', 'year', 'imdb', 'metascore', 'votes'])


def print_data(x):
    print(f'Displaying {x} data...')
    sleep(2)
    print(data_frame.head(x))
