from abc import ABC, abstractmethod

class IReuniao(ABC):
    @abstractmethod
    def mostrar_agenda(self, orientador_id, data):
        pass

    @abstractmethod
    def registrar_reuniao(self, aluno_id, orientador_id, data, hora_inicio, hora_fim, google_event_id=None):
        pass