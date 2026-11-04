from backend.interfaces.itarefa import ITarefa
from backend.cadastro import supabase

class Tarefa(ITarefa):
    def criar_tarefa(self, tcc_id, titulo, descricao):
        resposta = (
            supabase.table("tarefa").insert({
                "tcc_id": tcc_id,
                "titulo": titulo,
                "descricao": descricao,
                "status": "A_FAZER"
            }).execute()
        )

        return resposta.data

    def listar_tarefas(self, tcc_id):
        resposta = (
            supabase.table("tarefa").select("*").eq("tcc_id", tcc_id).order("data_criacao").execute()
        )

        return resposta.data

    def atualizar_status(self, tarefa_id, status):
        resposta = (
            supabase.table("tarefa").update({
                "status": status
            }).eq("id", tarefa_id).execute()
        )

        return resposta.data

    def buscar_tarefa(self, tarefa_id):
            resposta = (
                supabase.table("tarefa").select("*").eq("id", tarefa_id).execute()
            )
    
            return resposta.data[0]