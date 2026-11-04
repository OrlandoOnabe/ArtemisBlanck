from abc import ABC, abstractmethod

class ITarefa(ABC):
    @abstractmethod
    def criar_tarefa(self, tcc_id, titulo, descricao):
        pass

    @abstractmethod
    def listar_tarefas(self, tcc_id):
        pass

    @abstractmethod
    def atualizar_status(self, tarefa_id, status):
        pass

    @abstractmethod
    def buscar_tarefa(self, tarefa_id):
        pass