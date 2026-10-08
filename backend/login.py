import bcrypt

from backend.cadastro import supabase


def autenticar_usuario(email, senha, tipo_usuario):
    resposta = (
        supabase
        .table("usuario")
        .select("*")
        .eq("email", email)
        .eq("tipo", tipo_usuario)
        .execute()
    )

    if not resposta.data:
        return None

    usuario = resposta.data[0]

    if not bcrypt.checkpw(
        senha.encode("utf-8"),
        usuario["senha"].encode("utf-8")
    ):
        return None

    return usuario
