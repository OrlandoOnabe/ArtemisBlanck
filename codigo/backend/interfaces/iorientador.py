from abc import ABC, abstractmethod

class IOrientador(ABC):
    @abstractmethod
    def listar_orientadores(self):
        pass