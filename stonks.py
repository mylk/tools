#!/usr/bin/env python

import argparse
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from signal import signal, SIGINT
import sys
import time
import urwid

stock_defaults = ['aapl', 'tsla']
element_root = '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]'

# parse parameters
parser = argparse.ArgumentParser(description='List the price and % change of stonks.')
parser.add_argument('-i', '--interval', dest='interval', help='Interval in seconds to update the data', default=300, type=int)
parser.add_argument('-t', '--tickers', dest='tickers', help='Show specific stonk data. For multiple, comma-separate them', default='', type=str)
parser.add_argument('-u', '--update', dest='update', help='Update the data (every five minutes by default)', default=None, action='store_true')
args = parser.parse_args()


def get_webdriver():
    service = Service('/tmp/chromedriver')

    options = Options()
    options.headless = True
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent={}'.format(UserAgent().random))
    return webdriver.Chrome(options=options, service=service)


def build_elements(main_loop=None, data=None):
    global previous_results

    # set the current datetime
    last_update_txt = urwid.Text('')
    last_update_txt.set_text(datetime.now().strftime('%c'))

    results = crawl()
    elements = urwid.SimpleListWalker([])
    if not results:
        elements.append(urwid.Text('Could not fetch data.'))
    else:
        for result in results:
            elements.append(urwid.Text(result))

    elements_list = urwid.ListBox(elements)

    pile = urwid.Pile([last_update_txt, urwid.Divider(), (100, elements_list)])
    widget = urwid.Filler(pile, valign='top')
    main_loop.widget = widget

    # keep the results so the next crawl will compare prices to find out the trend
    previous_results = results


def schedule_and_build_elements(main_loop=None, data=None):
    build_elements(main_loop)

    main_loop.set_alarm_in(args.interval, schedule_and_build_elements)


# same as stonks.py, but without printing
def crawl():
    driver = get_webdriver()
    stocks = args.tickers.split(',') if args.tickers else stock_defaults

    items = []

    accepted_terms = False
    for stock in stocks:
        try:
            driver.get('https://finance.yahoo.com/quote/{}/'.format(stock))
        except Exception as ex:
            return []

        if not accepted_terms:
            # wait until the terms window is loaded
            # selenium.common.exceptions.TimeoutException
            WebDriverWait(driver, 30).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'form.consent-form button.btn.primary'))
            )
            driver.find_elements(By.CSS_SELECTOR, 'form.consent-form button.btn.primary')[0].click()
            accepted_terms = True

        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, '{}/div[1]/fin-streamer[1]'.format(element_root)))
        )
        price = driver.find_elements(By.XPATH, '{}/div[1]/fin-streamer[1]'.format(element_root))[0].text
        change_amount = driver.find_elements(By.XPATH, '{}/div/fin-streamer[2]/span'.format(element_root))[0].text
        change_percent = driver.find_elements(By.XPATH, '{}/div/fin-streamer[3]/span'.format(element_root))[0].text.replace('(', '').replace(')', '').replace('%', '')

        # check if there is an after hours div to wait for the values to load
        after_hours_div = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]/div[2]')
        if after_hours_div:
            WebDriverWait(driver, 120).until(
                expected_conditions.presence_of_element_located((By.XPATH, '{}/div[2]/fin-streamer[2]'.format(element_root)))
            )

        price_after_hours = driver.find_elements(By.XPATH, '{}/div[2]/fin-streamer[2]'.format(element_root))
        if price_after_hours:
            price_after_hours = price_after_hours[0].text

        change_off_hours_amount = driver.find_elements(By.XPATH, '{}/div[2]/span[1]/fin-streamer[1]/span'.format(element_root))
        if change_off_hours_amount:
            change_off_hours_amount = change_off_hours_amount[0].text

        change_off_hours_percent = driver.find_elements(By.XPATH, '{}/div[2]/span[1]/fin-streamer[2]/span'.format(element_root))
        if change_off_hours_percent:
            change_off_hours_percent = change_off_hours_percent[0].text.replace('(', '').replace(')', '').replace('%', '')

        if price_after_hours:
            price = price_after_hours
            change_amount = round(float(change_off_hours_amount) + float(change_amount), 2)
            # TypeError: float() argument must be a string or a real number, not 'list'
            change_percent = round(float(change_off_hours_percent) + float(change_percent), 2)

        # check if the stock price went up or down since the last crawl and choose a trend indicator
        trend = '-'
        for previous_result in previous_results:
            previous_result = previous_result.split()
            if previous_result[0].upper() == stock.upper():
                if float(price) > float(previous_result[1]):
                    trend = u'▲'
                elif float(price) < float(previous_result[1]):
                    trend = u'▼'

        items.append([stock, price, '{}%'.format(str(change_percent)), trend])

    results = list()
    # set the columns
    results.append('{:<5} {:<6} {:<7} {:<6}'.format('NAME', 'PRICE', 'CHANGE', 'TREND'))

    # set the data
    for item in items:
        name, price, change_percent, trend = item
        results.append('{:<5} {:<6} {:<7} {:<6}'.format(name.upper(), price, change_percent, trend))

    driver.close()

    return results


def handle_quit(key):
    if key in ['q', 'Q']:
        raise urwid.ExitMainLoop()
    elif key == 'u':
        build_elements(loop)


def handle_sigint(signal_received, frame):
    sys.exit(0)


if __name__ == '__main__':
    previous_results = []

    if not args.update:
        results = crawl()

        if not results:
            print('Could not fetch data.')
            sys.exit(1)

        for result in results:
            print(result)

        sys.exit(0)

    # call the handler when SIGINT is received
    signal(SIGINT, handle_sigint)

    pile = urwid.Pile([])
    widget = urwid.Filler(pile, valign='top')
    loop = urwid.MainLoop(widget, palette=[('reversed', 'standout', '')], unhandled_input=handle_quit)
    loop.set_alarm_in(args.interval, schedule_and_build_elements)

    build_elements(loop)

    loop.run()
