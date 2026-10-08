from backend.cadastro import supabase


def registrar_reuniao(aluno_id,orientador_id,data,hora_inicio,hora_fim,google_event_id=None):
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
