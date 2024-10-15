from smtplib import SMTP_SSL
from email.message import EmailMessage
from os import getenv


def enviar(
    email_destino: str,
    assunto: str,
    conteudo: str,
) -> None:
    try:
        email_origem = getenv("EMAIL")
        senha_origem = getenv("SENHA")
        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = email_origem
        msg["To"] = email_destino
        msg.set_content(conteudo)
        with SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_origem, senha_origem)
            smtp.send_message(msg)
        return True
    except Exception as e:
        return False
