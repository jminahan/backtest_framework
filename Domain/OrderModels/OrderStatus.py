from Domain.OrderModels.Contract import Contract
from Domain.OrderModels.Order import Order
from dataclasses import dataclass


from dataclasses import dataclass
from enum import Enum

class OrderStatuses(Enum):
    FILLED = "FILLED"
    UNFILLED = "UNFILLED"

@dataclass
class OrderStatus():
    status : str
    cost : int
    order : Order
    contract : Contract