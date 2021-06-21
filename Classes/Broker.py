from Enums import PredictorOrders
from __future__ import annotations
from AbstractClasses.ObserverPattern import Observer


class Broker(Observer):
    def __init__(self, maker_commission_fee=0.0, taker_commission_fee=0.0, balance=10):
        self._maker_commission_fee = maker_commission_fee
        self._taker_commission_fee = taker_commission_fee
        self._owned_assets = 0
        self._balance = balance

    def sell(self, price):
        if not self._owned_asset == 0:
            temp = self._owned_asset * price
            self.balance += temp - temp * self._taker_comission_fee
            self._owned_assets = 0

    def buy(self, price):
        if not self._available_funds == 0:
            taker_fee = self._available_funds * self._maker_commission_fee
            self._owned_assets += (self._balance - taker_fee) / price
            self._balance = 0

    def update(self, data:dict(order=PredictorOrders, price=float)):
        if data["order"] == PredictorOrders.BUY:
            self.buy(data["price"])
        if data["order"] == PredictorOrders.SELL:
            self.sell(data["price"])
