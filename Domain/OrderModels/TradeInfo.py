from dataclasses import dataclass
from Domain.OrderModels.Order import Order
from Domain.OrderModels.Contract import Contract
import logging

@dataclass
class TradeInfo():
    order : Order
    contract : Contract

    @staticmethod
    def fromjson(data):
        return TradeInfo(order = Order.fromjson(data["order"]),
        contract=Contract.fromjson(data["contract"]))

    def tojson(self):
        retDict = {}
        retDict["contract"] = self.contract.tojson()
        retDict["order"] = self.order.tojson()

        return retDict
