
from abc import ABC, abstractmethod

class VotingStrategy(ABC):
    @abstractmethod
    def vote():
        pass