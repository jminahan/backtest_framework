from dataclasses import dataclass
from enum import Enum
import logging

class OrderActions(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderTypes(Enum):
    MKT = "MKT"
    LIMIT = "LMT"

@dataclass
class Order():
    order_type: str
    total_quantity : int
    action : str

    @staticmethod
    def fromjson(data):
        if( data["order_type"] == OrderTypes.MKT):
            order_type = OrderTypes.MKT
        elif( data["order_type"] == OrderTypes.LIMIT):
            order_type = OrderTypes.LIMIT

        if(data["action"] == OrderActions.BUY):
            action = OrderActions.BUY
        elif(data["action"] == OrderActions.SELL):
            action = OrderActions.SELL
            
        return Order(
            order_type=order_type,
            total_quantity=data["total_quantity"],
            action=action
        )

    def tojson(self):
        retDict = {}
        retDict["order_type"] = self.order_type
        retDict["total_quantity"] = self.total_quantity
        retDict["action"] = self.action

        return retDict