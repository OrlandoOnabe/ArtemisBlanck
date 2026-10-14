from unittest.mock import MagicMock, patch
from backend.componentes.reuniao import Reuniao

def test_mostrar_agenda():
    mock_orientador = MagicMock()

    mock_orientador.listar_orientadores.return_value = [
        {
            "usuario_id": 1,
            "area_atuacao": "Inteligência Artificial",
            "vagas": 2
        }
    ]

    componente = Reuniao(mock_orientador)

    with patch(
        "backend.componentes.reuniao.gerar_horarios_disponiveis",
        return_value=["08:00", "08:30", "09:00"]
    ):

        resultado = componente.mostrar_agenda(1, "2026-10-20")

        assert resultado == ["08:00", "08:30", "09:00"]
        
        
def test_registrar_reuniao():
    mock_orientador = MagicMock()
    resposta = MagicMock()

    resposta.data = [
        {
            "id": 1,
            "aluno_id": 5,
            "orientador_id": 1,
            "data": "2026-10-20",
            "hora_inicio": "10:00",
            "hora_fim": "10:30",
            "status": "AGENDADA",
            "google_event_id": "evento123"
        }
    ]

    componente = Reuniao(mock_orientador)

    with patch("backend.componentes.reuniao.supabase") as mock_supabase:

        mock_supabase.table.return_value.insert.return_value.execute.return_value = resposta

        resultado = componente.registrar_reuniao(
            5,
            1,
            "2026-10-20",
            "10:00",
            "10:30",
            "evento123"
        )

        assert resultado[0]["status"] == "AGENDADA"
        assert resultado[0]["aluno_id"] == 5
        assert resultado[0]["orientador_id"] == 1