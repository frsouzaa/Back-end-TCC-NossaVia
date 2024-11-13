from ..db.database import Usuario as UsuarioModel


def atualizar(id_usuario: int, soma: int, db_session):
    usuario = (
        db_session.query(UsuarioModel)
        .filter(UsuarioModel.id == id_usuario, UsuarioModel.delete == False)
        .one()
    )
    usuario.pontuacao += soma
    db_session.add(usuario)
    db_session.flush()
