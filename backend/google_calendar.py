from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from backend.cadastro import supabase
import json


with open("credentials_web.json", "r") as arquivo:
    GOOGLE_CONFIG = json.load(arquivo)["web"]

CLIENT_ID = GOOGLE_CONFIG["client_id"]
CLIENT_SECRET = GOOGLE_CONFIG["client_secret"]
TOKEN_URI = GOOGLE_CONFIG["token_uri"]

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


def salvar_credenciais(orientador_id, credenciais):

    dados = {
        "orientador_id": orientador_id,
        "access_token": credenciais.token,
        "refresh_token": credenciais.refresh_token,
        "token_uri": credenciais.token_uri,
        "client_id": credenciais.client_id,
        "client_secret": credenciais.client_secret,
        "scopes": " ".join(credenciais.scopes)
    }

    supabase.table("google_calendar").upsert(
        dados,
        on_conflict="orientador_id"
    ).execute()


def obter_credenciais(orientador_id):

    resposta = (
        supabase
        .table("google_calendar")
        .select("*")
        .eq("orientador_id", orientador_id)
        .execute()
    )

    if not resposta.data:
        return None

    dados = resposta.data[0]

    credenciais = Credentials(
        token=dados["access_token"],
        refresh_token=dados["refresh_token"],
        token_uri=dados["token_uri"],
        client_id=dados["client_id"],
        client_secret=dados["client_secret"],
        scopes=dados["scopes"].split()
    )

    return credenciais

def criar_servico(orientador_id):

    credenciais = obter_credenciais(orientador_id)

    if credenciais is None:
        return None

    if credenciais.expired and credenciais.refresh_token:

        credenciais.refresh(Request())

        supabase.table("google_calendar").update({
            "access_token": credenciais.token
        }).eq(
            "orientador_id",
            orientador_id
        ).execute()

    return build(
        "calendar",
        "v3",
        credentials=credenciais
    )
    
def consultar_ocupados(orientador_id, inicio, fim):
    service = criar_servico(orientador_id)

    if service is None:
        return None

    corpo = {
        "timeMin": inicio.isoformat(),
        "timeMax": fim.isoformat(),
        "timeZone": "America/Sao_Paulo",
        "items": [
            {
                "id": "primary"
            }
        ]
    }

    resposta = (
        service
        .freebusy()
        .query(body=corpo)
        .execute()
    )

    return resposta["calendars"]["primary"]["busy"]

def gerar_horarios_disponiveis(orientador_id,data):
    inicio_dia = datetime.fromisoformat(
        f"{data}T08:00:00-03:00"
    )

    fim_dia = datetime.fromisoformat(
        f"{data}T18:00:00-03:00"
    )

    ocupados = consultar_ocupados(
        orientador_id,
        inicio_dia,
        fim_dia
    )

    if ocupados is None:
        return None

    horarios = []

    atual = inicio_dia

    while atual + timedelta(minutes=30) <= fim_dia:

        final = atual + timedelta(minutes=30)

        livre = True

        for ocupado in ocupados:

            inicio_ocupado = datetime.fromisoformat(
                ocupado["start"].replace(
                    "Z",
                    "+00:00"
                )
            )

            fim_ocupado = datetime.fromisoformat(
                ocupado["end"].replace(
                    "Z",
                    "+00:00"
                )
            )

            if (
                atual < fim_ocupado
                and final > inicio_ocupado
            ):
                livre = False
                break

        if livre:
            horarios.append(
                atual.strftime("%H:%M")
            )

        atual += timedelta(minutes=30)

    return horarios

def criar_evento(orientador_id, nome_aluno, email_aluno, data, hora_inicio):
    service = criar_servico(orientador_id)

    inicio = datetime.fromisoformat(
        f"{data}T{hora_inicio}:00-03:00"
    )

    fim = inicio + timedelta(minutes=30)

    evento = {
        "summary": "Reunião de TCC - Artemis",

        "description": (
            f"Reunião agendada pelo Artemis com {nome_aluno}."
        ),

        "start": {
            "dateTime": inicio.isoformat(),
            "timeZone": "America/Sao_Paulo"
        },

        "end": {
            "dateTime": fim.isoformat(),
            "timeZone": "America/Sao_Paulo"
        }
    }

    evento_criado = (
        service
        .events()
        .insert(
            calendarId="primary",
            body=evento
        )
        .execute()
    )

    return evento_criado
