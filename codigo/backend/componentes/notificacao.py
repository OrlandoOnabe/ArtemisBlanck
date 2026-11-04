import os
from brevo import Brevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)
from brevo.core.api_error import ApiError
from dotenv import load_dotenv
from backend.interfaces.inotificacao import INotificacao
load_dotenv()

class Email(INotificacao):
    def __init__(self):
        api_key = os.getenv("BREVO_API_KEY")
        self.cliente = Brevo(api_key=api_key)

    def enviar_email(self, destinatario, assunto, conteudo):

        try:
            resposta = self.cliente.transactional_emails.send_transac_email(
                subject=assunto,
                html_content=conteudo,

                sender=SendTransacEmailRequestSender(
                    name="Artemis",
                    email="orlandonagrockis@gmail.com"
                ),

                to=[
                    SendTransacEmailRequestToItem(
                        email=destinatario
                    )
                ]
            )

            return resposta

        except ApiError as erro:
            print("Erro ao enviar e-mail:", erro)
            return None