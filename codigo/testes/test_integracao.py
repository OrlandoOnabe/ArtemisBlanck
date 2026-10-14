from unittest.mock import patch, MagicMock
from backend.componentes.orientador import Orientador
from backend.componentes.reuniao import Reuniao

def test_integracao_reuniao_orientador():
    resposta = MagicMock()

    resposta.data = [
        {
            "usuario_id": 1,
            "area_atuacao": "Inteligência Artificial",
            "vagas": 2,
            "usuario": {
                "nome": "Orlando",
                "email": "orlando@fei.edu.br"
            }
        }
    ]

    with patch("backend.componentes.orientador.supabase") as mock_supabase:
        mock_supabase.table.return_value.select.return_value.execute.return_value = resposta
        componente_orientador = Orientador()
        componente_reuniao = Reuniao(componente_orientador)

        with patch(
            "backend.componentes.reuniao.gerar_horarios_disponiveis",
            return_value=["10:00", "10:30"]
        ):

            resultado = componente_reuniao.mostrar_agenda(
                1,
                "2026-10-20"
            )

            assert resultado == ["10:00", "10:30"]
