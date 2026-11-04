from backend.interfaces.itcc import ITCC
from backend.cadastro import supabase

class TCC(ITCC):
    def cadastrar_tcc(self, titulo, descricao, aluno_id, orientador_id):
        resposta = (
            supabase.table("tcc").insert({
                "titulo": titulo,
                "descricao": descricao,
                "aluno_id": aluno_id,
                "orientador_id": orientador_id,
            }).execute()
        )
        return resposta.data