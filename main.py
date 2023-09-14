##
## EPITECH PROJECT, 2023
## B-CNA-410-MPL-4-1-trade-hippolyte.aubert
## File description:
## main
##

#!/usr/bin/python3
# -*- coding: iso-8859-1 -*

""" Python starter bot for the Crypto Trader games, from ex-Riddles.io """
__version__ = "1.0"

import sys
import numpy as np

class Bot:
    def __init__(self):
        self.botState = BotState()
        self.bought = False
        self.stop_loss = 0
        self.take_profit = 0

    def run(self):
        while True:
            reading = input()
            if len(reading) == 0:
                continue
            self.parse(reading)

    def parse(self, info: str):
        tmp = info.split(" ")
        if tmp[0] == "settings":
            self.botState.update_settings(tmp[1], tmp[2])
        if tmp[0] == "update":
            if tmp[1] == "game":
                self.botState.update_game(tmp[2], tmp[3])
        if tmp[0] == "action":
            dollars = self.botState.stacks["USDT"]
            current_closing_price = self.botState.charts["USDT_BTC"].closes[-1]
            affordable = dollars / current_closing_price * 1.5

            close_prices = np.array(self.botState.charts["USDT_BTC"].closes)
            window_size = 20
            rsi = self.calculate_rsi(close_prices, window_size)

            print(f'My stacks are {dollars}. The current closing price is {current_closing_price}. So I can afford {affordable}', file=sys.stderr)

            if self.bought:
                if current_closing_price >= self.take_profit or current_closing_price <= self.stop_loss:
                    sell_amount = self.botState.stacks["BTC"]
                    print(f'sell USDT_BTC {sell_amount}', flush=True)
                    self.bought = False
                else:
                    print("no_moves", flush=True)
            else:
                if dollars < 100:
                    print("no_moves", flush=True)
                else:
                    last_high = max(close_prices[-20:])
                    if current_closing_price <= last_high * 0.9:
                        buy_amount = 0.1 * affordable
                        self.stop_loss = current_closing_price * 0.95
                        self.take_profit = current_closing_price * 1.02
                        print(f'buy USDT_BTC {buy_amount}', flush=True)
                        self.bought = True
                    else:
                        print("no_moves", flush=True)

    def calculate_rsi(self, prices, window_size):
        deltas = np.diff(prices)
        seed = deltas[:window_size + 1]
        up = seed[seed >= 0].sum() / window_size
        down = -seed[seed < 0].sum() / window_size
        rs = up / down
        rsi = np.zeros_like(prices)
        rsi[:window_size] = 100.0 - (100.0 / (1.0 + rs))

        for i in range(window_size, len(prices)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.0
            else:
                upval = 0.0
                downval = -delta

            up = (up * (window_size - 1) + upval) / window_size
            down = (down * (window_size - 1) + downval) / window_size
            rs = up / down
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))
        return rsi[-1]

class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        for (i, key) in enumerate(format):
            value = tmp[i]
            if key == "pair":
                self.pair = value
            if key == "date":
                self.date = int(value)
            if key == "high":
                self.high = float(value)
            if key == "low":
                self.low = float(value)
            if key == "open":
                self.open = float(value)
            if key == "close":
                self.close = float(value)
            if key == "volume":
                self.volume = float(value)

    def __repr__(self):
        return str(self.pair) + str(self.date) + str(self.close) + str(self.volume)

class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)


class BotState:
    def __init__(self):
        self.timeBank = 0
        self.maxTimeBank = 0
        self.timePerMove = 1
        self.candleInterval = 1
        self.candleFormat = []
        self.candlesTotal = 0
        self.candlesGiven = 0
        self.initialStack = 0
        self.transactionFee = 0.1
        self.date = 0
        self.stacks = dict()
        self.charts = dict()

    def update_chart(self, pair: str, new_candle_str: str):
        if not (pair in self.charts):
            self.charts[pair] = Chart()
        new_candle_obj = Candle(self.candleFormat, new_candle_str)
        self.charts[pair].add_candle(new_candle_obj)

    def update_stack(self, key: str, value: float):
        self.stacks[key] = value

    def update_settings(self, key: str, value: str):
        if key == "timebank":
            self.maxTimeBank = int(value)
            self.timeBank = int(value)
        if key == "time_per_move":
            self.timePerMove = int(value)
        if key == "candle_interval":
            self.candleInterval = int(value)
        if key == "candle_format":
            self.candleFormat = value.split(",")
        if key == "candles_total":
            self.candlesTotal = int(value)
        if key == "candles_given":
            self.candlesGiven = int(value)
        if key == "initial_stack":
            self.initialStack = int(value)
        if key == "transaction_fee_percent":
            self.transactionFee = float(value)

    def update_game(self, key: str, value: str):
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
        if key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))


if __name__ == "__main__":
    mybot = Bot()
    mybot.run()