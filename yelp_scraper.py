#!/usr/bin/env python

# Basic Yelp scraper. Input city to find list of top rated restaurants. If you can't use the yelp app on your phone and like using command line...

from bs4 import BeautifulSoup
import requests						# for getting web pages
import pandas as pd

def main():
	city = raw_input('What city do you want to search? ')
	print 'Searching for restaurants in {}...'.format(city)
	link = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc={}'.format(''.join(city.split()))
	results, names, ratings, prices, categories = scrape_yelp(link)
	print pd.DataFrame({'Name': names})

	while True:
		try:
			index = input('Input an index 0-9 to learn more information... or enter anything to exit. ')
			if index >= 0 and index <= 9:
				display_more_info(index, results, ratings, prices, categories)
			else:
				raise ValueError()
		except Exception as e:
			exit()

def to_string(list):
	return [item.get_text() for item in list]

# Gets yelp results page for the input city and parses relevant information (restaurant names, ratings, prices, categories)
def scrape_yelp(link):
	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	content = soup.find(class_='search-results-content')
	results = content.find_all(class_='regular-search-result')
	names = [nt.get_text() for nt in content.select('.regular-search-result .search-result-title a')]
	ratings = [r['title'] for r in content.select('.regular-search-result .i-stars')]
	prices = [pt.get_text().strip() for pt in content.select('.regular-search-result .bullet-after')]
	cat_tags = [result.select('.category-str-list a') for result in results]
	categories = [to_string(ct) for ct in cat_tags]

	return results, names, ratings, prices, categories

def display_phone(phone):
	print 'Phone Number: {}'.format(phone.strip())

def display_addr(address):
	print 'Address: {}'.format(address.strip())

def display_rating(rating):
	print 'Rating: {}'.format(rating)

def display_price(price):
	print 'Price Range: {}'.format(price)

def display_category(cats):
	print 'Category: {}'.format(','.join(cats))

def display_more_info(index, results, ratings, prices, categories):
	secondary = results[index].find(class_='secondary-attributes')
	phone = secondary.find(class_='biz-phone').get_text()
	addr = secondary.find('address').get_text()
	rating = ratings[index]
	price = prices[index]
	cats = categories[index]
	display_phone(phone)
	display_addr(addr)
	display_rating(rating)
	display_price(price)
	display_category(cats)

if __name__ == "__main__":
    main()