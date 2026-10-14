from backend.cadastro import supabase
from backend.interfaces.iorientador import IOrientador


class Orientador(IOrientador):

    def listar_orientadores(self):
        resposta = (
            supabase
            .table("orientador")
            .select(
                "usuario_id, area_atuacao, vagas, usuario(nome, email)"
            )
            .execute()
        )
        return resposta.data