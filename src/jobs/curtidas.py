from src.db.database import db_session, Curtida, Reclamacao
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_
from os import getenv


def run():
    print(f"{"Job Curtidas":-^47}")
    print(f"Iniciando execução - {datetime.now()}")
    
    now = datetime.now()
    day_minus_one = date(now.year, now.month, now.day) - timedelta(days=int(getenv("DIAS_JOB")))
    
    print(f"Buscando desde {day_minus_one}")

    ids_reclamacoes = [i[0] for i in (
        db_session.query(Reclamacao.id)
        .join(Curtida, Curtida.reclamacao_id == Reclamacao.id)
        .where(
            or_(Curtida.criacao >= day_minus_one, Curtida.modificacao >= day_minus_one)
        )
        .group_by(Reclamacao.id)
        .all()
    )]
    
    reclamacoes = (
        db_session.query(Reclamacao, func.count(Reclamacao.id))
        .join(Curtida, Curtida.reclamacao_id == Reclamacao.id)
        .where(
            Reclamacao.id.in_(ids_reclamacoes),
            Curtida.delete == False,
        )
        .group_by(Reclamacao.id)
        .all()
    )
    
    for reclamacao in reclamacoes:
        reclamacao[0].qtd_curtidas = reclamacao[1]
        db_session.add(reclamacao[0])

    db_session.commit()
    
    print(f"Fim da execução - {datetime.now()}")
