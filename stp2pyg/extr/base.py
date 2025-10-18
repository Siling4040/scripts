from abc import ABC, abstractmethod

class AttrExtrBase(ABC):
    @abstractmethod
    def face(self, face):
        pass

    @abstractmethod
    def edge(self, edge):
        pass
