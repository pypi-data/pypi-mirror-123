from Project.celeb_births_scraper import Scraper
from Project.celeb_births_date import Date   


date_object = Date(27, 3, 1991)
scraper = Scraper()
celebrities = scraper.get_celebrities('February_30')
print(celebrities)