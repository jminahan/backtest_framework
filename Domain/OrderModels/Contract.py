from dataclasses import dataclass
import enum
from enum import Enum

class ContractSecurityTypes(Enum):
    STOCK = "STK"

class ContractPrimaryExchanges(Enum):
    NASDAQ = "NASDAQ"

class ContractCurrencies(Enum):
    USD = "USD"
class ContractExchanges(Enum):
    SMART = "SMART"

@dataclass
class Contract():
    symbol: str
    sec_type : str
    prim_exchange : str
    exchange : str
    currency : str