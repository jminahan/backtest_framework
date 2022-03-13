from abc import ABC, abstractmethod
from this import d

class BaseAdapter(ABC):
    freeCapital : float
    def __init__(self):
        pass
    
    def getFreeCapital(self) -> float:
        return self.freeCapital