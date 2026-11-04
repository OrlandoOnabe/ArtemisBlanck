from abc import ABC, abstractmethod

class INotificacao(ABC):
    @abstractmethod
    def enviar_email(self, destinatario, assunto, conteudo):
        pass