from abc import ABC, abstractmethod

class IFeedback(ABC):
    @abstractmethod
    def registrar_feedback(self, tarefa_id, orientador_id, texto):
        pass

    @abstractmethod
    def listar_feedbacks(self, tarefa_id):
        pass
