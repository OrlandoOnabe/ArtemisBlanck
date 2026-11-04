from backend.componentes.notificacao import Email


componente_notificacao = Email()

resultado = componente_notificacao.enviar_email(
    destinatario="pggleme@protonmail.com",
    assunto="Teste Artemis",
    conteudo="""
        <h2>Artemis</h2>
        <p>Tranque o curso</p>
    """
)

print(resultado)