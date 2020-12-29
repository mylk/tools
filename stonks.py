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
import sys

stock_defaults = ['aapl', 'tsla']

items = []

arguments = sys.argv[1:]
stocks = arguments if arguments else stock_defaults

for stock in stocks:
    response = requests.get('https://finance.yahoo.com/quote/{}/'.format(stock))
    soup = BeautifulSoup(response.text, 'html.parser')

    price = soup.select('[data-locator="subtree-root"] [data-reactid="32"]')[1].string
    price_after_hours = soup.select('[data-locator="subtree-root"] [data-reactid="37"]')[1].string
    if price_after_hours:
        price = price_after_hours

    changes = soup.select('[data-locator="subtree-root"] [data-reactid="33"]')[2].string.split(' ')[1].replace('(', '').replace(')', '').replace('%', '')
    changes_off_hours = soup.select('#quote-header-info > [data-reactid="29"] [data-reactid="36"] [data-reactid="40"]')
    if changes_off_hours:
        changes_off_hours = changes_off_hours[0].string.split(' ')[1].replace('(', '').replace(')', '').replace('%', '')
        changes = round(float(changes_off_hours) + float(changes), 2)

    items.append([stock, price, '{}%'.format(str(changes))])

# print the names of the columns
print ("{:<6} {:<6} {:<6}".format('NAME', 'PRICE', 'CHANGE'))

# print each data item
for item in items:
    name, price, change = item
    print ("{:<6} {:<6} {:<6}".format(name.upper(), price, change))

