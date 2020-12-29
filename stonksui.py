#!/usr/bin/env python

from bs4 import BeautifulSoup
from datetime import datetime
import requests
from signal import signal, SIGINT
import sys
import urwid

stock_defaults = ['aapl', 'tsla']


def build_elements(main_loop=None, data=None):
    global previous_results

    elements.clear()

    # add the current datetime
    last_update_txt = urwid.Text('')
    last_update_txt.set_text(datetime.now().strftime('%c'))
    elements.append(last_update_txt)
    elements.append(urwid.Text(''))

    results = crawl()
    for result in results:
        elements.append(urwid.Text(result))

    # keep the results so the next crawl will compare prices to find out the trend
    previous_results = results

    # this will throw an error the first time is ran
    try:
        loop.set_alarm_in(300, build_elements)
    except NameError:
        pass


# same as stonks.py, but without printing
def crawl():
    arguments = sys.argv[1:]
    stocks = arguments if arguments else stock_defaults

    items = []

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

        # check if the stock price went up or down since the last crawl and choose a trend indicator
        trend = '-'
        for previous_result in previous_results:
            previous_result = previous_result.split()
            if previous_result[0].upper() == stock.upper():
                if float(price) > float(previous_result[1]):
                    trend = u'▲'
                elif float(price) < float(previous_result[1]):
                    trend = u'▼'

        items.append([stock, price, '{}%'.format(str(changes)), trend])

    results = list()
    # set the columns
    results.append('{:<5} {:<6} {:<7} {:<6}'.format('NAME', 'PRICE', 'CHANGE', 'TREND'))

    # set the data
    for item in items:
        name, price, change, trend = item
        results.append('{:<5} {:<6} {:<7} {:<6}'.format(name.upper(), price, change, trend))

    return results


def handle_quit(key):
    if key in ['q', 'Q']:
        raise urwid.ExitMainLoop()


def handle_sigint(signal_received, frame):
    sys.exit(0)


if __name__ == '__main__':
    # call the handler when SIGINT is received
    signal(SIGINT, handle_sigint)

    previous_results = []
    elements = urwid.SimpleListWalker([])
    build_elements()

    main = urwid.ListBox(elements)

    top = urwid.Overlay(
        main,
        urwid.SolidFill(),
        align='left',
        width=('relative', 30),
        valign='top',
        height=('relative', 50),
        min_width=20,
        min_height=5
    )

    loop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')], unhandled_input=handle_quit)
    loop.set_alarm_in(300, build_elements)
    loop.run()
