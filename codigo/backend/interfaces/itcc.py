from abc import ABC, abstractmethod

class ITCC(ABC):
    @abstractmethod
    def cadastrar_tcc(self, titulo, descricao, aluno_id, orientador_id):
        pass