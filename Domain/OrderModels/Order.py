from dataclasses import dataclass
from enum import Enum

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