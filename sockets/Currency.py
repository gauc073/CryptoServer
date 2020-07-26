class CurrencyView:
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
