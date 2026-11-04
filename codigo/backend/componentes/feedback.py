from backend.interfaces.ifeedback import IFeedback
from backend.cadastro import supabase

class Feedback(IFeedback):
    def registrar_feedback(self, tarefa_id, orientador_id, texto):
        resposta = (
            supabase.table("feedback").insert({
                "tarefa_id": tarefa_id,
                "orientador_id": orientador_id,
                "texto": texto
            }).execute()
        )

        return resposta.data


    def listar_feedbacks(self, tarefa_id):
        resposta = (
            supabase.table("feedback").select("*").eq("tarefa_id", tarefa_id).order("data_criacao").execute()
        )

        return resposta.data