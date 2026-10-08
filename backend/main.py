import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from backend.cadastro import cadastrar_aluno, cadastrar_orientador, supabase
from backend.login import autenticar_usuario
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import Flow
from backend.reuniao import registrar_reuniao
from backend.google_calendar import (SCOPES, salvar_credenciais, gerar_horarios_disponiveis, criar_evento)
from datetime import datetime, timedelta


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="uma-chave-secreta-qualquer"
)

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def inicio():
    return RedirectResponse(url="/login")


@app.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/cadastro/aluno")
def pagina_cadastro_aluno(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cadastro_aluno.html"
    )


@app.get("/cadastro/orientador")
def pagina_cadastro_orientador(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cadastro_orientador.html"
    )


@app.post("/cadastro/aluno")
def inserir_aluno(request: Request, nome: str = Form(...), cpf: str = Form(...), telefone: str = Form(...), ra: str = Form(...), email: str = Form(...), senha: str = Form(...),):


    resultado = cadastrar_aluno(
        nome,
        cpf,
        telefone,
        ra,
        email,
        senha
    )

    if not resultado["sucesso"]:
        return templates.TemplateResponse(
            request=request,
            name="cadastro_aluno.html",
            context={
                "erro": resultado["mensagem"],
                "campo_erro": resultado["campo"]
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="cadastro_aluno.html",
        context={
            "sucesso": "Cadastro realizado com sucesso!"
        }
    )

@app.post("/cadastro/orientador")
def inserir_orientador(request: Request, nome: str = Form(...), cpf: str = Form(...), telefone: str = Form(...), email: str = Form(...), area_atuacao: str = Form(...), vagas: int = Form(...), senha: str = Form(...),):

    resultado = cadastrar_orientador(
        nome,
        cpf,
        telefone,
        email,
        area_atuacao,
        vagas,
        senha
    )

    if not resultado["sucesso"]:
        return templates.TemplateResponse(
            request=request,
            name="cadastro_orientador.html",
            context={
                "erro": resultado["mensagem"],
                "campo_erro": resultado["campo"]
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="cadastro_orientador.html",
        context={
            "sucesso": "Cadastro realizado com sucesso!"
        }
    )

@app.post("/login")
def fazer_login(request: Request, email: str = Form(...), senha: str = Form(...), tipo_usuario: str = Form(...)):
    usuario = autenticar_usuario(
        email,
        senha,
        tipo_usuario
    )

    if usuario is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "erro": "E-mail ou senha inválido"
            }
        )
        
    request.session["usuario_id"] = usuario["id"]
    request.session["tipo"] = usuario["tipo"]

    if usuario["tipo"] == "ALUNO":
        return RedirectResponse(
            url="/central/aluno",
            status_code=303
        )

    return RedirectResponse(
        url="/central/orientador",
        status_code=303
    )


@app.get("/central/aluno")
def central_aluno(request: Request):
    usuario_id = request.session.get("usuario_id")
    resposta_usuario = (
        supabase
        .table("usuario")
        .select("id, nome, cpf, telefone, email, tipo")
        .eq("id", usuario_id)
        .single()
        .execute()
    )

    resposta_aluno = (
        supabase
        .table("aluno")
        .select("ra")
        .eq("usuario_id", usuario_id)
        .single()
        .execute()
    )
    usuario = resposta_usuario.data
    aluno = resposta_aluno.data
    return templates.TemplateResponse(
        request=request,
        name="central_aluno.html",
        context={"usuario": usuario, "aluno": aluno}
    )


@app.get("/central/orientador")
def central_orientador(request: Request):
    usuario_id = request.session.get("usuario_id")
    resposta_usuario = (
        supabase
        .table("usuario")
        .select("id, nome, cpf, telefone, email, tipo")
        .eq("id", usuario_id)
        .single()
        .execute()
    )

    resposta_orientador = (
        supabase
        .table("orientador")
        .select("area_atuacao, vagas")
        .eq("usuario_id", usuario_id)
        .single()
        .execute()
    )
    usuario = resposta_usuario.data
    orientador = resposta_orientador.data
    return templates.TemplateResponse(
        request=request,
        name="central_orientador.html",
        context={"usuario": usuario, "orientador": orientador}
    )


@app.get("/orientadores")
def lista_orientadores(request: Request):
    resposta = (
        supabase
        .table("orientador")
        .select("usuario_id, area_atuacao, vagas, usuario(nome, email)")
        .execute()
    )
    orientadores = resposta.data
    return templates.TemplateResponse(
        request=request,
        name="lista_orientadores.html",
        context={"orientadores": orientadores}
    )


@app.get("/orientador/{orientador_id}")
def pagina_orientador(request: Request, orientador_id: int):

    aluno_id = request.session.get("usuario_id")

    if aluno_id is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    resposta_usuario = (
        supabase
        .table("usuario")
        .select("id, nome, email, telefone")
        .eq("id", orientador_id)
        .eq("tipo", "ORIENTADOR")
        .single()
        .execute()
    )

    resposta_orientador = (
        supabase
        .table("orientador")
        .select("area_atuacao, vagas")
        .eq("usuario_id", orientador_id)
        .single()
        .execute()
    )

    resposta_reunioes = (
        supabase
        .table("reuniao")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("orientador_id", orientador_id)
        .eq("status", "AGENDADA")
        .order("data")
        .order("hora_inicio")
        .execute()
    )

    return templates.TemplateResponse(
        request=request,
        name="orientador.html",
        context={
            "usuario": resposta_usuario.data,
            "orientador": resposta_orientador.data,
            "reunioes": resposta_reunioes.data
        }
    )
    
@app.get("/google/conectar")
def conectar_google(request: Request):

    flow = Flow.from_client_secrets_file(
        "credentials_web.json",
        scopes=SCOPES,
        autogenerate_code_verifier=True
    )

    flow.redirect_uri = (
        "http://127.0.0.1:8000/google/callback"
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    request.session["google_state"] = state

    request.session["google_code_verifier"] = (
        flow.code_verifier
    )

    return RedirectResponse(
        authorization_url
    )
    
    
@app.get("/google/callback")
def google_callback(request: Request):
    usuario_id = request.session.get("usuario_id")
    state = request.session.get("google_state")

    code_verifier = request.session.get(
        "google_code_verifier"
    )

    flow = Flow.from_client_secrets_file(
        "credentials_web.json",
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = (
        "http://127.0.0.1:8000/google/callback"
    )

    flow.code_verifier = code_verifier

    flow.fetch_token(
        authorization_response=str(request.url)
    )

    credenciais = flow.credentials

    salvar_credenciais(
        usuario_id,
        credenciais
    )

    request.session.pop(
        "google_state",
        None
    )

    request.session.pop(
        "google_code_verifier",
        None
    )

    return RedirectResponse(
        url="/central/orientador",
        status_code=303
    )
    
@app.get("/orientador/{orientador_id}/agenda")
def agenda_orientador(request: Request, orientador_id: int, data: str = None):

    resposta = (
        supabase
        .table("usuario")
        .select("id, nome")
        .eq("id", orientador_id)
        .single()
        .execute()
    )

    orientador = resposta.data

    horarios = None
    calendar_conectado = True

    if data:
        horarios = gerar_horarios_disponiveis(
            orientador_id,
            data
        )
        if horarios is None:
            calendar_conectado = False

    return templates.TemplateResponse(
        request=request,
        name="agenda.html",
        context={
            "orientador": orientador,
            "orientador_id": orientador_id,
            "data": data,
            "horarios": horarios,
            "calendar_conectado": calendar_conectado
        }
    )
    
@app.post("/orientador/{orientador_id}/agendar")
def agendar_reuniao(request: Request, orientador_id: int, data: str = Form(...), hora: str = Form(...)):

    aluno_id = request.session.get("usuario_id")

    horarios = gerar_horarios_disponiveis(
        orientador_id,
        data
    )

    if horarios is None or hora not in horarios:
        return RedirectResponse(
            url=f"/orientador/{orientador_id}/agenda?data={data}",
            status_code=303
        )

    resposta_aluno = (
        supabase
        .table("usuario")
        .select("nome, email")
        .eq("id", aluno_id)
        .single()
        .execute()
    )

    aluno = resposta_aluno.data

    evento = criar_evento(
        orientador_id,
        aluno["nome"],
        aluno["email"],
        data,
        hora
    )

    hora_inicio = hora

    inicio = datetime.strptime(
        hora,
        "%H:%M"
    )

    fim = inicio + timedelta(
        minutes=30
    )

    hora_fim = fim.strftime(
        "%H:%M"
    )

    registrar_reuniao(
        aluno_id,
        orientador_id,
        data,
        hora_inicio,
        hora_fim,
        evento["id"]
    )

    return RedirectResponse(
        url="/central/aluno",
        status_code=303
    )
    
@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )
