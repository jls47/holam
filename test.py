from holam import Reader
from holam import exScrape
from holam import portScrape

crawler = exScrape("en_US", "europe")
#crawler = portScrape("en_US", "asia")
crawler.visit()
