#!/usr/bin/env python

import argparse
import curses
from datetime import datetime
import json
import requests
from signal import signal, SIGINT
import sys
import texttable
import time

# parse parameters
parser = argparse.ArgumentParser(description='List the price and % change of cryptocurrencies.')
parser.add_argument('-b', '--borders', dest='borders', help='Show borders', default=None, action='store_true')
parser.add_argument('-i', '--interval', dest='interval', help='Interval in seconds to update the data', default=60, type=int)
parser.add_argument('-s', '--symbols', dest='symbols', help='Show specific coin data. For multiple, comma-separate them', default='', type=str)
parser.add_argument('-t', '--top', dest='coins_count', help='Show the X top coins by market cap', default=5, type=int)
parser.add_argument('-u', '--update', dest='update', help='Update the data (every minute by default)', default=None, action='store_true')
args = parser.parse_args()

show_borders = texttable.Texttable.BORDER | texttable.Texttable.HLINES | texttable.Texttable.VLINES if args.borders else 0
symbols = [] if not args.symbols else list(map(str.lower, args.symbols.split(',')))


def get_data():
    response = requests.get('https://api.coincap.io/v2/assets?limit={}'.format(args.coins_count))
    data = json.loads(response.text)['data']
    return data


def draw_table(data):
    table = texttable.Texttable()
    table.set_cols_width([14, 10, 10])
    table.set_deco(show_borders)

    columns = ['NAME', 'PRICE ($)', 'CHANGE']
    table.add_row(columns)

    for row in data:
        # no symbols selected or selected symbol matches the currently iterated
        if not symbols or (symbols and row['symbol'].lower() in symbols):
            table.add_row([
                '{} ({})'.format(row['name'], row['symbol']),
                row['priceUsd'],
                '{}%'.format(round(float(row['changePercent24Hr']), 2))
            ])

    return table.draw()


def handle_sigint(signal_received, frame):
    curses.curs_set(1)
    curses.endwin()
    sys.exit(0)


if __name__ == '__main__':
    if not args.update:
        data = get_data()
        table = draw_table(data)

        print(table)

        sys.exit(0)

    # call the handler when SIGINT is received
    signal(SIGINT, handle_sigint)

    # initialize the curses screen
    screen = curses.initscr()
    curses.curs_set(0)
    
    while True:
        data = get_data()
        table = draw_table(data)

        last_update = datetime.now().strftime('%c')
        screen.addstr(0, 0, last_update)
        screen.addstr(2, 0, table)
        screen.refresh()

        time.sleep(args.interval)
