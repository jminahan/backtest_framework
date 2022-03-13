from dataclasses import dataclass
from Domain.OrderModels.Order import Order
from Domain.OrderModels.Contract import Contract

@dataclass
class TradeInfo():
    order : Order
    contract : Contract
