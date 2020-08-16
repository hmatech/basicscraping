from scraper.detik_com import *
from scraper.imdb1 import *
from scraper.nama_studios import *


def run():
    print('+' * 30)
    print('+Basic web scraping, searching for product')
    print('+Target: NAMA - Indonesia')
    print('+Created by Habibie Muhammad A')
    print('+' * 30)
    print('Example of keyword: \n'
          '\tVX, Lite, Card Case, Stark, etc')
    search_product()


def mulai():
    print('Scraping sederhana website detik.com')
    pilihanprogram = (int(input('Mau cari apa?\n'
                                '1. Tag Terpopuler\n'
                                '2. Berita terpopuler\n'
                                'Masukkan pilihan (angka): ')))
    if pilihanprogram == 1:
        cari_tag()
    elif pilihanprogram == 2:
        cari_berita_populer()
    else:
        print('Maaf pilihan tidak ada!')


def proceed():
    confirm = input(f'You are going to scrape approximately up to {imdb1.movie_total} movies data.\n'
                    f'Proceed?(Y/N): ')
    if confirm == 'Y' or confirm == 'y':
        movie_scraper()
        append_data()
        print_data(10)
    elif confirm == 'N' or confirm == 'n':
        print('Cancelling...')
    else:
        print('That option is not exist!')
