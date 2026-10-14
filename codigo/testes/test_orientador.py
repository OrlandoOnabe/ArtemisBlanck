from unittest.mock import MagicMock, patch
from backend.componentes.orientador import Orientador

def test_listar_orientadores():
    dados = [
        {
            "usuario_id": 1,
            "area_atuacao": "Inteligência Artificial",
            "vagas": 2,
            "usuario": {
                "nome": "Morgana",
                "email": "morgana@fei.edu.br"
            }
        },
        {
            "usuario_id": 2,
            "area_atuacao": "Banco de Dados",
            "vagas": 1,
            "usuario": {
                "nome": "Orlando",
                "email": "orlando@fei.edu.br"
            }
        }
    ]

    resposta = MagicMock()
    resposta.data = dados

    with patch("backend.componentes.orientador.supabase") as mock_supabase:
        mock_supabase.table.return_value.select.return_value.execute.return_value = resposta
        componente = Orientador()
        resultado = componente.listar_orientadores()

        assert resultado == dados
        assert len(resultado) == 2
        assert resultado[0]["usuario"]["nome"] == "Morgana"
        assert resultado[0]["vagas"] == 2