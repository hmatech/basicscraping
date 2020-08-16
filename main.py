"""
By Habibie Muhammad A
habibiemuhammad90@gmail.com
"""

import scraper as sc

print("Simple scraping with Beautiful Soup 4")
cho = int(input("What target would you like to scrape?\n"
                "1. Nama-Studios\n"
                "2. Detik.com\n"
                "3. IMDb.com\n"
                "Enter your choice (number): "))
if cho == 1:
    sc.run()
elif cho == 2:
    sc.mulai()
elif cho == 3:
    sc.proceed()
else:
    print("Sorry, that choice isn't exist")
