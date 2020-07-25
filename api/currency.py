#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:09:35 2019
@author: gaurava
"""

import json
from flask import jsonify
import requests


class Currency:
    def __init__(self):
        self.id = "cur_id"
        self.fullName = "full_name"
        self.ask = "0"
        self.bid = "0"
        self.last = "0"
        self.open = "0"
        self.low = "0"
        self.high = "0"
        self.feeCurrency = "fee_currency"

    def set_symbol_details(self, cur_id, fee_currency):
        self.id = cur_id
        self.feeCurrency = fee_currency

    def set_ticker_details(self, ask, bid, last, day_open, low, high):
        self.ask = ask
        self.bid = bid
        self.last = last
        self.open = day_open
        self.low = low
        self.high = high

    def set_currency_details(self, full_name):
        self.fullName = full_name


def get_currency_details_by_symbol(symbol):
    url = "https://api.hitbtc.com/api/2/public/symbol/" + symbol
    symbol_response = requests.get(url)
    if symbol_response.status_code != 200:
        json_response_text = json.loads(symbol_response.text)
        return jsonify(json_response_text), 400

    url = "https://api.hitbtc.com/api/2/public/ticker/" + symbol
    tickers_response = requests.get(url)
    if tickers_response.status_code != 200:
        json_response_text = json.loads(tickers_response.text)
        return jsonify(json_response_text), 400

    ticker_object = json.loads(tickers_response.text)
    symbol_object = json.loads(symbol_response.text)
    cur_id = symbol_object["baseCurrency"]
    url = "https://api.hitbtc.com/api/2/public/currency/" + cur_id
    currencies_response = requests.get(url)
    if currencies_response.status_code != 200:
        json_response_text = json.loads(currencies_response.text)
        return jsonify(json_response_text), 400

    currency_object = json.loads(currencies_response.text)
    currency_obj = Currency()
    currency_obj.set_symbol_details(symbol_object["id"], symbol_object["feeCurrency"])
    currency_obj.set_ticker_details(ticker_object["ask"], ticker_object["bid"], ticker_object["last"],
                                    ticker_object["open"], ticker_object["low"], ticker_object["high"])
    currency_obj.set_currency_details(currency_object["fullName"])
    return jsonify(currency_obj.__dict__), 200


def get_all_currency_details():
    url = "https://api.hitbtc.com/api/2/public/symbol/"
    symbol_response = requests.get(url)
    if symbol_response.status_code != 200:
        json_response_text = json.loads(symbol_response.text)
        return jsonify(json_response_text), 400

    url = "https://api.hitbtc.com/api/2/public/ticker/"
    tickers_response = requests.get(url)
    if tickers_response.status_code != 200:
        json_response_text = json.loads(tickers_response.text)
        return jsonify(json_response_text), 400

    url = "https://api.hitbtc.com/api/2/public/currency"
    currencies_response = requests.get(url)
    if currencies_response.status_code != 200:
        json_response_text = json.loads(currencies_response.text)
        return jsonify(json_response_text), 400

    currencies_details_map = dict()
    currency_base_currency_mapping = dict()
    symbols_obj = json.loads(symbol_response.text)
    tickers_obj = json.loads(tickers_response.text)
    currencies_obj = json.loads(currencies_response.text)
    for each in symbols_obj:
        # create mapping between base currency and its all derived symbols
        new_list = currency_base_currency_mapping.get(each["baseCurrency"], [])
        new_list.append(each["id"])
        currency_base_currency_mapping[each["baseCurrency"]] = new_list
        currency = Currency()
        currency.set_symbol_details(each["id"], each["feeCurrency"])
        currencies_details_map[currency.id] = currency

    for each in tickers_obj:
        symbol = each["symbol"]
        if symbol in currencies_details_map:
            currency: Currency = currencies_details_map[symbol]
            currency.set_ticker_details(each["ask"], each["bid"], each["last"],
                                        each["open"], each["low"], each["high"])
    for each in currencies_obj:
        cur_id = each["id"]
        if cur_id in currency_base_currency_mapping:
            # print(currency_base_currency_mapping[cur_id])
            for each_sub_cur in currency_base_currency_mapping[cur_id]:
                if each_sub_cur in currencies_details_map:
                    currency: Currency = currencies_details_map[each_sub_cur]
                    # print(each["fullName"])
                    currency.set_currency_details(each["fullName"])

    list_of_currencies = []
    for each in currencies_details_map.values():
        list_of_currencies.append(each.__dict__)
    return jsonify(list_of_currencies), 200
