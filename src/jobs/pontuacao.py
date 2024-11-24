from src.db.database import db_session, Curtida, Reclamacao, Comentario, Usuario
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_
from os import getenv


def run():
    print(f"{"Job Pontuação":-^47}")
    print(f"Iniciando execução - {datetime.now()}")
    
    now = datetime.now()
    day_minus_one = date(now.year, now.month, now.day) - timedelta(days=int(getenv("DIAS_JOB")))
    
    print(f"Buscando desde {day_minus_one}")

    usuarios_reclamacoes = {
        i[0]
        for i in (
            db_session.query(Reclamacao.usuario_id)
            .where(
                or_(
                    Reclamacao.criacao >= day_minus_one,
                    Reclamacao.modificacao >= day_minus_one,
                )
            )
            .all()
        )
    }

    res = {
        i
        for i in (
            db_session.query(Reclamacao.usuario_id, Curtida.usuario_id)
            .join(Curtida, Curtida.reclamacao_id == Reclamacao.id)
            .where(
                or_(
                    Curtida.criacao >= day_minus_one,
                    Curtida.modificacao >= day_minus_one,
                ),
                Curtida.usuario_id != Reclamacao.usuario_id,
            )
            .all()
        )
    }
    
    usuarios_curtidas = set()
    for i in res:
        usuarios_curtidas.add(i[0])
        usuarios_curtidas.add(i[1])

    res = {
        i
        for i in (
            db_session.query(Reclamacao.usuario_id, Comentario.usuario_id)
            .join(Comentario, Comentario.reclamacao_id == Reclamacao.id)
            .where(
                or_(
                    Comentario.criacao >= day_minus_one,
                    Comentario.modificacao >= day_minus_one,
                ),
                Comentario.usuario_id != Reclamacao.usuario_id,
            )
            .all()
        )
    }
    
    usuarios_comentarios = set()
    for i in res:
        usuarios_comentarios.add(i[0])
        usuarios_comentarios.add(i[1])

    reclamacoes_por_usuario = (
        db_session.query(Reclamacao.usuario_id, func.count(Reclamacao.id))
        .where(
            Reclamacao.usuario_id.in_(usuarios_reclamacoes), Reclamacao.delete == False
        )
        .group_by(Reclamacao.usuario_id)
        .all()
    )

    curtidas_por_usuario = (
        db_session.query(
            Curtida.usuario_id, func.count(Curtida.usuario_id), Reclamacao.usuario_id
        )
        .join(Reclamacao, Curtida.reclamacao_id == Reclamacao.id)
        .where(
            or_(
                Curtida.usuario_id.in_(usuarios_curtidas),
                Reclamacao.usuario_id.in_(usuarios_curtidas),
            ),
            Curtida.usuario_id != Reclamacao.usuario_id,
            Curtida.delete == False,
        )
        .group_by(Curtida.usuario_id, Reclamacao.usuario_id)
        .all()
    )

    # Equivalente em SQL:
    # select c.usuario_id, count(c.usuario_id) as curtidas, r.usuario_id from curtida c
    # join reclamacao r
    #     on c.reclamacao_id = r.id
    # where c."delete" = false
    #     and c.usuario_id != r.usuario_id
    # group by c.usuario_id, r.usuario_id

    comentarios_por_usuario = (
        db_session.query(
            Comentario.usuario_id,
            func.count(Comentario.usuario_id),
            Reclamacao.usuario_id,
        )
        .join(Reclamacao, Comentario.reclamacao_id == Reclamacao.id)
        .where(
            or_(
                Comentario.usuario_id.in_(usuarios_comentarios),
                Reclamacao.usuario_id.in_(usuarios_comentarios),
            ),
            Comentario.usuario_id != Reclamacao.usuario_id,
            Comentario.delete == False,
        )
        .group_by(Comentario.usuario_id, Reclamacao.usuario_id)
        .all()
    )

    # Equivalente em SQL:
    # select c.usuario_id, count(c.usuario_id) as comentarios, r.usuario_id from comentario c
    # join reclamacao r
    #     on c.reclamacao_id = r.id
    # where c."delete" = false
    #     and c.usuario_id != r.usuario_id
    # group by c.usuario_id, r.usuario_id
    # order by c.usuario_id;

    set_usuario = usuarios_reclamacoes.union(usuarios_curtidas).union(
        usuarios_comentarios
    )

    usuarios_com_curtidas = (
        db_session.query(Usuario).where(Usuario.id.in_(set_usuario)).all()
    )

    pontos_por_usuario = {i: 0 for i in set_usuario}
        
    PONTOS_RECLAMACAO = int(getenv("PONTOS_RECLAMACAO"))
    PONTOS_COMENTARIO = int(getenv("PONTOS_COMENTARIO"))
    PONTOS_CURTIDA = int(getenv("PONTOS_CURTIDA"))

    for reclamacao in reclamacoes_por_usuario:
        if reclamacao[0] in set_usuario:
            pontos_por_usuario[reclamacao[0]] += reclamacao[1] * PONTOS_RECLAMACAO

    for curtida in curtidas_por_usuario:
        if curtida[0] in set_usuario:
            pontos_por_usuario[curtida[0]] += curtida[1] * PONTOS_CURTIDA
        if curtida[2] in set_usuario:
            pontos_por_usuario[curtida[2]] += curtida[1] * PONTOS_CURTIDA
        
    for comentario in comentarios_por_usuario:
        if comentario[0] in set_usuario:
            pontos_por_usuario[comentario[0]] += comentario[1] * PONTOS_COMENTARIO
        if comentario[2] in set_usuario:
            pontos_por_usuario[comentario[2]] += comentario[1] * PONTOS_COMENTARIO

    for usuario in usuarios_com_curtidas:
        if usuario.pontuacao != pontos_por_usuario[usuario.id]:
            print(
                f"Identificada diferença na pontuação do usuario {usuario.id}, mundando de {usuario.pontuacao} para {pontos_por_usuario[usuario.id]}"
            )
            usuario.pontuacao = pontos_por_usuario[usuario.id]
            db_session.add(usuario)

    db_session.commit()
    
    print(f"Fim da execução - {datetime.now()}")
