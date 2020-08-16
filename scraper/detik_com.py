import requests as rq
from bs4 import BeautifulSoup
import datetime as dt
import webbrowser as wb

hariini = dt.date.today()


def open_link(link):
    wb.open(link)


def req_link():
    url = 'https://www.detik.com'
    req = rq.get(url)
    print('Meminta...')
    if req.status_code == 200:
        print('Sukses! Kode status: ', req.status_code)
        return req
    else:
        print('Ada error!')


def buka_link(kumpulanlink):
    while True:
        pilihan = int(input('Apa yang ingin anda buka?(Masukkan nomor): '))
        try:
            list_pilihan = [1, 2, 3, 4, 5]
            if pilihan in list_pilihan:
                link = kumpulanlink[pilihan - 1]
                print(f'Membuka link ke {pilihan}...')
                open_link(link)
                break
            else:
                print('Pilihan tidak ada!')
        except ValueError:
            print('Harap masukkan nomor!')
            continue


def cari_tag():
    obj = req_link()
    sup = BeautifulSoup(obj.content, 'lxml')
    detikpopulertag = sup.find_all('div', class_='terpopuler')
    print(f'Mencari popular tag per {hariini}')
    kumplink = []
    for tag in detikpopulertag:
        populer = tag.find_all('a')
        print('Ditemukan: ', (len(populer)))
        urutan = 0
        for pop in populer:
            pops = pop.get('onclick').split('"')
            poplink = pop.get('href')
            kumplink.append(poplink)
            print(f'{urutan+1}. {pops[3]}')
            urutan += 1
    buka_link(kumplink)


def cari_berita_populer():
    obj = req_link()
    sup = BeautifulSoup(obj.content, 'lxml')
    print(f'Mencari berita terpopuler per {hariini}')
    beritaterpopuler = sup.find_all('div', class_='cb-mostpop')
    kumpulanlink = []
    for berita in beritaterpopuler:
        beritas = berita.find_all('a')
        urutan = 0
        for listberita in beritas:
            satu = listberita.get('onclick').split('"')
            link = listberita.get('href')
            kumpulanlink.append(link)
            onclickindex = satu[3]
            if onclickindex != 'selengkapnya':
                print(f'{urutan+1}. {onclickindex}')
            urutan += 1
    buka_link(kumpulanlink)
