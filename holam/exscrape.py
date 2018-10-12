from bs4 import BeautifulSoup, Tag
import csv
import urllib.request
import pandas as pd
from selenium import webdriver
import time
from langdetect import detect

class exScrape(object):
	def __init__(self, lang, region):
		self.lang = lang
		self.region = region
		self.details = {}
	
	def visit(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors-spki-list')
		options.add_argument('--ignore-ssl-errors')
		driver = webdriver.Chrome(options=options)
		details = {}
		driver.get("https://www.hollandamerica.com")
		dropdown = driver.find_element_by_class_name('dropdown-label')
		dropdown.click()
		items = driver.find_elements_by_class_name('dropdown-item')
		if "de" in self.lang:
			for item in items:
				if '-3' in str(item):
					item.click()
		elif "es" in self.lang:
			for item in items:
				if '-4' in str(item):
					item.click()
		elif "nl" in self.lang:
			for item in items:
				if '-5' in str(item):
					item.click()
		
		url = "https://www.hollandamerica.com/"+self.lang+"/cruise-destinations/"+self.region+".excursions.html#sort=name%20asc&start=0&rows=12?"
		driver.get(url)
		page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
		pages = int(driver.find_element_by_class_name("total-pages").get_attribute("innerText"))
		
		print(pages)
		while page < (pages-1):
			time.sleep(1)
			page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
			next = driver.find_elements_by_class_name("next")
			print(next)
			links = driver.find_elements_by_class_name("see-details-cta-label")
			for link in links:
				details[(link.get_attribute("href"))] = {}
			if len(next) != 0:
				next[0].click()
				
		time.sleep(1)
		page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
		next = driver.find_elements_by_class_name("next")
		print(next)
		links = driver.find_elements_by_class_name("see-details-cta-label")
		for link in links:
			details[(link.get_attribute("href"))] = {}
		
		
		for url in details:
			driver.get(url + "?")
			title = driver.find_element_by_class_name("title").get_attribute("innerText")
			details[url]["title"] = title
			
			heroimg = driver.find_elements_by_class_name("image-lazy-loader")
			details[url]["translated"] = "n"
			if len(heroimg) != 0:
				heroimg = driver.find_element_by_class_name("image-lazy-loader")
				if "sunset-water" in heroimg.find_element_by_tag_name("img").get_attribute("src"):
					details[url]["hero image"] = "n"
				details[url]["hero image"] = "y"
			else:
				details[url]["hero image"] = "n"
			
			facts = driver.find_elements_by_class_name("shorex-key-facts")
			if len(facts) != 0:
				details[url]["details"] = "y"
			else: 
				details[url]["details"] = "n"
				
			desc = driver.find_elements_by_class_name("desc")
			if len(desc) != 0:
				details[url]["description"] = "y"
				if "en" not in self.lang and len(desc[0].find_elements_by_tag_name("p")) != 0:
					text = desc[0].find_element_by_tag_name("p").get_attribute("innerText")
					tlang = detect(text)
					if tlang in self.lang:
						details[url]["translated"] = "y"
					else:
						details[url]["translated"] = "n"
			else: 
				details[url]["description"] = "n"
				details[url]["translated"] = "n"
		
		if "en" in self.lang:
			with open(self.lang+".txt", "a") as enfile:
				enfile.write(details)
			with open(self.lang+".csv", "w", newline="") as csvfile:
				exwriter = csv.writer(csvfile)
				exwriter.writerow(["Hero Image", "Details", "Description", "Name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["details"], details[key]["description"], details[key]["title"], str(key)])
		else:
			data = ""
			with open('new.txt', 'r') as newfile:
				data = newfile.read().replace('\n', '').replace("en_US", self.lang)
				print(data)
			for url in details:
				string = url
				print(string)
				if string in data:
					details[url]["ineng"] = "y"
				else:
					details[url]["ineng"] = "n"
				
		print(details)
		
		with open(self.lang+".csv", "w", newline="") as csvfile:
			exwriter = csv.writer(csvfile)
			if self.lang == "en_US":
				exwriter.writerow(["Hero Image", "Details", "Description", "Name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["details"], details[key]["description"], details[key]["title"], str(key)])
			else:
				exwriter.writerow(["Hero Image", "Details", "Description", "in en", "translated", "name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["details"], details[key]["description"], details[key]["ineng"], details[key]["translated"], details[key]["title"], str(key)])
			
		
		