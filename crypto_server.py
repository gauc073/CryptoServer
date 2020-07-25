#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask
from api.currency import *
# Instantiate the Node
app = Flask(__name__)


@app.route('/currency/<symbol>', methods=['GET'])
def fetch_symbol_details(symbol):
    return get_currency_details_by_symbol(symbol)


@app.route('/currency/all', methods=['GET'])
def fetch_all_symbol_details():
    return get_all_currency_details()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    print("Author   : Gaurav Agarwal")
    print("Application : CryptoServer Application")
    print("")
    app.run(host='0.0.0.0', port=port)
