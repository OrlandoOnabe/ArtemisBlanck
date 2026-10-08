from supabase import create_client
import bcrypt

SUPABASE_URL = "URL"
SUPABASE_KEY = "KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def cadastrar_aluno(nome, cpf, telefone, ra, email, senha):
    validar_cpf = (supabase.table("usuario").select("id").eq("cpf", cpf).execute())

    if validar_cpf.data:
        return {
            "sucesso": False,
            "campo": "cpf",
            "mensagem": "Este CPF já está cadastrado."
        }
        
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

    resposta_usuario = supabase.table("usuario").insert({
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "senha": senha_hash.decode("utf-8"),
        "tipo": "ALUNO"
    }).execute()

    usuario_id = resposta_usuario.data[0]["id"]

    supabase.table("aluno").insert({
        "usuario_id": usuario_id,
        "ra": ra
    }).execute()

    return {
        "sucesso": True,
        "mensagem": "Aluno cadastrado com sucesso"
    }


def cadastrar_orientador(nome, cpf, telefone, email, area_atuacao, vagas, senha):
    validar_cpf = (supabase.table("usuario").select("id").eq("cpf", cpf).execute())
    
    if validar_cpf.data:
        return {
            "sucesso": False,
            "campo": "cpf",
            "mensagem": "Este CPF já está cadastrado."
        }
            
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

    resposta_usuario = supabase.table("usuario").insert({
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "senha": senha_hash.decode("utf-8"),
        "tipo": "ORIENTADOR"
    }).execute()

    usuario_id = resposta_usuario.data[0]["id"]

    supabase.table("orientador").insert({
        "usuario_id": usuario_id,
        "area_atuacao": area_atuacao,
        "vagas": vagas
    }).execute()

    return {
        "sucesso": True,
        "mensagem": "Orientador cadastrado com sucesso"
    }
