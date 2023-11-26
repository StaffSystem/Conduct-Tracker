from abc import ABC, abstractmethod


class DownVote(ABC):
    @abstractmethod
    def vote():
        pass