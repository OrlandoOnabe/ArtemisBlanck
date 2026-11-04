from abc import ABC, abstractmethod

class IOrientador(ABC):
    @abstractmethod
    def listar_orientadores(self, area_atuacao = None):
        pass

    @abstractmethod
    def verificar_vagas(self, orientador_id):
        pass

    @abstractmethod
    def atualizar_vaga(self, orientador_id):
        pass