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

    @staticmethod
    def fromjson(data):
        if(data["sec_type"] == ContractSecurityTypes.STOCK):
            sec_type = ContractSecurityTypes.STOCK

        if(data["prim_exchange"] == ContractPrimaryExchanges.NASDAQ):
            prim_exchange = ContractPrimaryExchanges.NASDAQ

        if(data["exchange"] == ContractExchanges.SMART):
            exchange = ContractExchanges.SMART


        if(data["currency"] == ContractCurrencies.USD):
            currency = ContractCurrencies.USD

        return Contract(
            symbol=data["symbol"],
            sec_type=sec_type,
            prim_exchange=prim_exchange,
            exchange=exchange,
            currency=currency
        )

    def tojson(self):
        retDict = {}
        retDict["symbol"] = self.symbol
        retDict["sec_type"] = self.sec_type
        retDict["prim_exchange"] = self.prim_exchange
        retDict["exchange"] = self.exchange
        retDict["currency"] = self.currency

        return retDict