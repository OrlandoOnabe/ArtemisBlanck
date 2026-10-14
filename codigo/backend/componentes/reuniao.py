from backend.cadastro import supabase
from backend.google_calendar import gerar_horarios_disponiveis

from backend.interfaces.ireuniao import IReuniao
from backend.interfaces.iorientador import IOrientador


class Reuniao(IReuniao):

    def __init__(self, orientador: IOrientador):
        self.orientador = orientador


    def mostrar_agenda(self, orientador_id, data):
        return gerar_horarios_disponiveis(
            orientador_id,
            data
        )


    def registrar_reuniao(self, aluno_id, orientador_id, data, hora_inicio, hora_fim, google_event_id=None):
        resposta = (
            supabase
            .table("reuniao")
            .insert({
                "aluno_id": aluno_id,
                "orientador_id": orientador_id,
                "data": data,
                "hora_inicio": hora_inicio,
                "hora_fim": hora_fim,
                "status": "AGENDADA",
                "google_event_id": google_event_id
            })
            .execute()
        )
        return resposta.data