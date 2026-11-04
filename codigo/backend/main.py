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
from backend.componentes.orientador import Orientador
from backend.componentes.reuniao import Reuniao
from backend.google_calendar import SCOPES, salvar_credenciais, criar_evento
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from backend.componentes.tcc import TCC
from backend.componentes.tarefa import Tarefa
from backend.componentes.feedback import Feedback
from backend.componentes.notificacao import Email

app = FastAPI()

componente_orientador = Orientador()
componente_reuniao = Reuniao(componente_orientador)
componente_tcc = TCC()
componente_tarefa = Tarefa()
componente_feedback = Feedback()
componente_notificacao = Email()

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
    return templates.TemplateResponse(request=request, name="login.html")


@app.get("/cadastro/aluno")
def pagina_cadastro_aluno(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro_aluno.html")


@app.get("/cadastro/orientador")
def pagina_cadastro_orientador(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro_orientador.html")


@app.post("/cadastro/aluno")
def inserir_aluno(request: Request, nome: str = Form(...), cpf: str = Form(...), telefone: str = Form(...), ra: str = Form(...), email: str = Form(...), senha: str = Form(...)):
    resultado = cadastrar_aluno(nome, cpf, telefone, ra, email, senha)

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
def inserir_orientador(request: Request, nome: str = Form(...), cpf: str = Form(...), telefone: str = Form(...), email: str = Form(...), area_atuacao: str = Form(...), vagas: int = Form(...), senha: str = Form(...)):
    resultado = cadastrar_orientador(nome, cpf, telefone, email, area_atuacao, vagas, senha)

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
    usuario = autenticar_usuario(email, senha, tipo_usuario)

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
        return RedirectResponse(url="/central/aluno", status_code=303)

    return RedirectResponse(url="/central/orientador", status_code=303)


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

    resposta_tcc = (
        supabase
        .table("tcc")
        .select(
            "id, titulo, descricao, orientador_id, "
            "orientador(usuario(nome))"
        )
        .eq("aluno_id", usuario_id)
        .execute()
    )

    tcc = resposta_tcc.data[0] if resposta_tcc.data else None
    usuario = resposta_usuario.data
    aluno = resposta_aluno.data

    return templates.TemplateResponse(
        request=request,
        name="central_aluno.html",
        context={
            "usuario": usuario,
            "aluno": aluno,
            "tcc": tcc
        }
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

    resposta_tccs = (
        supabase
        .table("tcc")
        .select(
            "id, titulo, descricao, aluno_id, "
            "aluno(usuario(nome, email))"
        )
        .eq("orientador_id", usuario_id)
        .execute()
    )

    tccs = resposta_tccs.data
    usuario = resposta_usuario.data
    orientador = resposta_orientador.data

    return templates.TemplateResponse(
        request=request,
        name="central_orientador.html",
        context={
            "usuario": usuario,
            "orientador": orientador,
            "tccs": tccs
        }
    )


@app.get("/orientadores")
def lista_orientadores(request: Request, area_atuacao: str = None):
    orientadores = componente_orientador.listar_orientadores(area_atuacao)

    return templates.TemplateResponse(
        request=request,
        name="lista_orientadores.html",
        context={
            "orientadores": orientadores,
            "filtro": area_atuacao
        }
    )


@app.get("/orientador/{orientador_id}")
def pagina_orientador(request: Request, orientador_id: int):
    aluno_id = request.session.get("usuario_id")
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
    flow = Flow.from_client_secrets_file("credentials_web.json", scopes=SCOPES, autogenerate_code_verifier=True)
    flow.redirect_uri = "http://127.0.0.1:8000/google/callback"
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true", prompt="consent")

    request.session["google_state"] = state
    request.session["google_code_verifier"] = flow.code_verifier

    return RedirectResponse(authorization_url)


@app.get("/google/callback")
def google_callback(request: Request):

    usuario_id = request.session.get("usuario_id")
    state = request.session.get("google_state")
    code_verifier = request.session.get("google_code_verifier")

    flow = Flow.from_client_secrets_file("credentials_web.json", scopes=SCOPES, state=state)
    flow.redirect_uri = "http://127.0.0.1:8000/google/callback"
    flow.code_verifier = code_verifier
    flow.fetch_token(authorization_response=str(request.url))

    credenciais = flow.credentials

    salvar_credenciais(usuario_id, credenciais)

    request.session.pop("google_state", None)
    request.session.pop("google_code_verifier", None)

    return RedirectResponse(url="/central/orientador", status_code=303)


@app.get("/orientador/{orientador_id}/agenda")
def agenda_orientador(request: Request, orientador_id: int, data: str = None, erro: str = None):
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
    mensagem_erro = None

    if data:
        hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).date()
        data_selecionada = datetime.strptime(data, "%Y-%m-%d").date()

        if data_selecionada < hoje:
            horarios = []
            mensagem_erro = "Não é possível consultar horários de uma data passada."
        else:
            horarios = componente_reuniao.mostrar_agenda(orientador_id, data)
            if horarios is None:
                calendar_conectado = False

    if erro == "data_passada":
        mensagem_erro = "Não é possível agendar uma reunião em uma data ou horário que já passou."

    return templates.TemplateResponse(
        request=request,
        name="agenda.html",
        context={
            "orientador": orientador,
            "orientador_id": orientador_id,
            "data": data,
            "horarios": horarios,
            "calendar_conectado": calendar_conectado,
            "erro": mensagem_erro
        }
    )


@app.post("/orientador/{orientador_id}/agendar")
def agendar_reuniao(request: Request, orientador_id: int, data: str = Form(...), hora: str = Form(...)):
    data_hora_reuniao = datetime.strptime(
        f"{data} {hora}",
        "%Y-%m-%d %H:%M"
    ).replace(tzinfo=ZoneInfo("America/Sao_Paulo"))

    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    if data_hora_reuniao <= agora:
        return RedirectResponse(
            url=f"/orientador/{orientador_id}/agenda?data={data}&erro=data_passada",
            status_code=303
        )

    aluno_id = request.session.get("usuario_id")

    resposta_aluno = (
        supabase
        .table("usuario")
        .select("nome, email")
        .eq("id", aluno_id)
        .single()
        .execute()
    )

    aluno = resposta_aluno.data

    resposta_orientador = (
        supabase
        .table("usuario")
        .select("nome, email")
        .eq("id", orientador_id)
        .single()
        .execute()
    )

    orientador = resposta_orientador.data

    evento = criar_evento(orientador_id, aluno["nome"], aluno["email"], data, hora)

    hora_inicio = hora

    inicio = datetime.strptime(hora, "%H:%M")

    fim = inicio + timedelta(minutes=30)

    hora_fim = fim.strftime("%H:%M")

    componente_reuniao.registrar_reuniao(aluno_id, orientador_id, data, hora_inicio, hora_fim, evento["id"])

    componente_notificacao.enviar_email(
        destinatario=aluno["email"],
        assunto="Reunião agendada - Artemis",
        conteudo=f"""
            <h2>Olá, {aluno["nome"]}!</h2>

            <p>
                Sua reunião com o orientador
                <strong>{orientador["nome"]}</strong>
                foi agendada com sucesso.
            </p>

            <p>
                <strong>Data:</strong> {data}
            </p>

            <p>
                <strong>Horário:</strong> {hora_inicio} às {hora_fim}
            </p>
        """
    )

    componente_notificacao.enviar_email(
        destinatario=orientador["email"],
        assunto="Nova reunião agendada - Artemis",
        conteudo=f"""
            <h2>Olá, {orientador["nome"]}!</h2>

            <p>
                O aluno <strong>{aluno["nome"]}</strong>
                agendou uma reunião com você.
            </p>

            <p>
                <strong>Data:</strong> {data}
            </p>

            <p>
                <strong>Horário:</strong> {hora_inicio} às {hora_fim}
            </p>
        """
    )

    return RedirectResponse(url="/central/aluno", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/tcc/cadastrar")
def pagina_cadastro_tcc(request: Request):
    orientadores = componente_orientador.listar_orientadores()

    return templates.TemplateResponse(
        request=request,
        name="cadastro_tcc.html",
        context={
            "orientadores": orientadores
        }
    )

@app.post("/tcc/cadastrar")
def cadastrar_tcc(request: Request, titulo: str = Form(...), descricao: str = Form(...), orientador_id: int = Form(...)):
    aluno_id = request.session.get("usuario_id")

    if not componente_orientador.verificar_vagas(orientador_id):
        orientadores = componente_orientador.listar_orientadores()
        return templates.TemplateResponse(
            request=request,
            name="cadastro_tcc.html",
            context={
                "orientadores": orientadores,
                "erro": "O orientador selecionado não possui vagas disponíveis."
            }
        )

    componente_tcc.cadastrar_tcc(titulo=titulo, descricao=descricao, aluno_id=aluno_id, orientador_id=orientador_id)
    componente_orientador.atualizar_vaga(orientador_id)

    return RedirectResponse(
        url="/central/aluno",
        status_code=303
    )

@app.get("/tcc/{tcc_id}")
def acompanhar_tcc(request: Request, tcc_id: int):
    resposta_tcc = (
        supabase
        .table("tcc")
        .select(
            "id, titulo, descricao, "
            "aluno_id, orientador_id, "
            "aluno(usuario(nome)), "
            "orientador(usuario(nome))"
        )
        .eq("id", tcc_id)
        .execute()
    )

    tcc = resposta_tcc.data[0]
    usuario_id = request.session.get("usuario_id")
    pode_editar = usuario_id == tcc["aluno_id"]
    tarefas = componente_tarefa.listar_tarefas(tcc_id)

    tarefas_a_fazer = []
    tarefas_fazendo = []
    tarefas_feito = []

    for tarefa in tarefas:
        if tarefa["status"] == "A_FAZER":
            tarefas_a_fazer.append(tarefa)
        elif tarefa["status"] == "FAZENDO":
            tarefas_fazendo.append(tarefa)
        elif tarefa["status"] == "FEITO":
            tarefas_feito.append(tarefa)

    return templates.TemplateResponse(
        request=request,
        name="tcc.html",
        context={
            "tcc": tcc,
            "tarefas_a_fazer": tarefas_a_fazer,
            "tarefas_fazendo": tarefas_fazendo,
            "tarefas_feito": tarefas_feito,
            "pode_editar": pode_editar
        }
    )

@app.get("/tcc/{tcc_id}/tarefas/criar")
def pagina_criar_tarefa(request: Request, tcc_id: int):
    return templates.TemplateResponse(
        request=request,
        name="criar_tarefa.html",
        context={
            "tcc_id": tcc_id
        }
    )

@app.post("/tcc/{tcc_id}/tarefas/criar")
def criar_tarefa(request: Request,tcc_id: int,titulo: str = Form(...),descricao: str = Form("")):
    titulo = titulo.strip()
    descricao = descricao.strip()

    if not titulo:
        return templates.TemplateResponse(
            request=request,
            name="criar_tarefa.html",
            context={
                "tcc_id": tcc_id,
                "erro": "O título da tarefa é obrigatório."
            }
        )

    componente_tarefa.criar_tarefa(tcc_id=tcc_id, titulo=titulo, descricao=descricao)

    return RedirectResponse(
        url=f"/tcc/{tcc_id}",
        status_code=303
    )

@app.post("/tcc/{tcc_id}/tarefas/{tarefa_id}/status")
def atualizar_status_tarefa(request: Request, tcc_id: int, tarefa_id: int,novo_status: str = Form(...)):
    usuario_id = request.session.get("usuario_id")

    resposta_tcc = (
        supabase
        .table("tcc")
        .select("aluno_id")
        .eq("id", tcc_id)
        .execute()
    )
    if usuario_id != resposta_tcc.data[0]["aluno_id"]:
        return {
            "sucesso": False,
            "mensagem": "Apenas o aluno pode movimentar tarefas."
        }

    sucesso = componente_tarefa.atualizar_status(
        tarefa_id,
        novo_status
    )

    return {
        "sucesso": bool(sucesso)
    }

@app.get("/tcc/{tcc_id}/tarefas/{tarefa_id}")
def pagina_tarefa(request: Request,tcc_id: int,tarefa_id: int):
    tarefa = componente_tarefa.buscar_tarefa(tarefa_id)

    resposta_tcc = (
        supabase
        .table("tcc")
        .select("aluno_id, orientador_id")
        .eq("id", tcc_id)
        .execute()
    )

    tcc = resposta_tcc.data[0]
    usuario_id = request.session.get("usuario_id")
    orientador = usuario_id == tcc["orientador_id"]
    feedbacks = componente_feedback.listar_feedbacks(tarefa_id)

    return templates.TemplateResponse(
        request=request,
        name="tarefa.html",
        context={
            "tcc_id": tcc_id,
            "tarefa": tarefa,
            "feedbacks": feedbacks,
            "orientador": orientador
        }
    )

@app.post("/tcc/{tcc_id}/tarefas/{tarefa_id}/feedback")
def registrar_feedback(request: Request, tcc_id: int, tarefa_id: int, texto: str = Form(...)):
    usuario_id = request.session.get("usuario_id")
    texto = texto.strip()
    tarefa = componente_tarefa.buscar_tarefa(tarefa_id)

    if not texto:
        return templates.TemplateResponse(
            request=request,
            name="tarefa.html",
            context={
                "tcc_id": tcc_id,
                "tarefa": tarefa,
                "feedbacks": componente_feedback.listar_feedbacks(tarefa_id),
                "orientador": True,
                "erro": "O feedback não pode estar vazio."
            }
        )

    componente_feedback.registrar_feedback(tarefa_id=tarefa_id, orientador_id=usuario_id, texto=texto)

    resposta_tcc = (
            supabase.table("tcc").select(
                "titulo, aluno_id, orientador_id, "
                "aluno(usuario(nome, email))"
            ).eq("id", tcc_id).execute()
        )
    tcc = resposta_tcc.data[0]
    aluno = tcc["aluno"]["usuario"]
    nome_aluno = aluno["nome"]
    email_aluno = aluno["email"]

    componente_notificacao.enviar_email(
        destinatario=email_aluno,
        assunto="Novo feedback registrado - Artemis",
        conteudo=f"""
            <h2>Olá, {nome_aluno}!</h2>

            <p>
                Seu orientador registrou um novo feedback
                em uma tarefa do seu TCC.
            </p>

            <p>
                <strong>TCC:</strong> {tcc["titulo"]}
            </p>

            <p>
                <strong>Tarefa:</strong> {tarefa["titulo"]}
            </p>

            <p>
                Acesse o Artemis para visualizar o feedback.
            </p>
        """
    )

    return RedirectResponse(
        url=f"/tcc/{tcc_id}/tarefas/{tarefa_id}",
        status_code=303
    )