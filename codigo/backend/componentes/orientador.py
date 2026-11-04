from backend.cadastro import supabase
from backend.interfaces.iorientador import IOrientador


class Orientador(IOrientador):
    def listar_orientadores(self, area_atuacao = None):
        consulta = (
            supabase
            .table("orientador")
            .select(
                "usuario_id, area_atuacao, vagas, usuario(nome, email)"
            )
        )
        if area_atuacao != None:
            consulta = consulta.ilike("area_atuacao", f"%{area_atuacao}%")

        resposta = consulta.execute()
        return resposta.data

    def verificar_vagas(self, orientador_id):
        resposta = (
            supabase
            .table("orientador")
            .select("vagas")
            .eq("usuario_id", orientador_id)
            .execute()
        )

        vagas = resposta.data[0]["vagas"]
        return vagas > 0

    def atualizar_vaga(self, orientador_id):
        consulta = (
            supabase
            .table("orientador")
            .select("vagas")
            .eq("usuario_id", orientador_id)
            .single()
            .execute()
        )

        vagas_atuais = consulta.data["vagas"]
        (supabase.table("orientador").update({
                "vagas": vagas_atuais - 1
            }).eq("usuario_id", orientador_id).execute()
        )