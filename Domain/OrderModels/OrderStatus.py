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