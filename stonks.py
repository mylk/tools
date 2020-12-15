#!/usr/bin/env python

# Scrape Yahoo! Finance to get the current price and the percentage change of your stonks! 
#
# Requirements:
# pip install BeautifulSoup4
#
# Usage:
# ./stonks.py

from bs4 import BeautifulSoup
import requests

stocks = ['tsla', 'aapl']
items = []

for stock in stocks:
    response = requests.get('https://finance.yahoo.com/quote/{}/'.format(stock))
    soup = BeautifulSoup(response.text, 'html.parser')

    price = soup.select('[data-locator="subtree-root"] [data-reactid="32"]')[1].string
    
    changes = soup.select('[data-locator="subtree-root"] [data-reactid="33"]')[2].string
    change_percent = changes.split(' ')[1].replace('(', '').replace(')', '')

    items.append([stock, price, change_percent])

# print the names of the columns
print ("{:<6} {:<6} {:<6}".format('NAME', 'PRICE', 'CHANGE'))

# print each data item
for item in items:
    name, price, change = item
    print ("{:<6} {:<6} {:<6}".format(name.upper(), price, change))

