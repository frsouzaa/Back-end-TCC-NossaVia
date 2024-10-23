from src.db.database import Reclamacao
from sqlalchemy import func


def test_get_reclamacoes_proximas(client, login, database_session):
    # valores limite para uma reclamação ser considerada próxima (raio de 70m)
    longitudes = [
        60.00062882069886,
        60.00062882069887,  # valor limite
        60.00062882069888,
    ]
    i = 1
    for longitude in longitudes:
        reclamacao: Reclamacao = Reclamacao(
            "descricao",
            "via",
            "2024-10-03 19:47:00.000000",
            "12345-123",
            "rua teste",
            "123",
            "perto do teste",
            "bairro teste",
            "cidade teste",
            "PI",
            0,
            longitude,
            "",
            0,
            i + 1,
            "nao_resolvido",
            None,
            func.ST_SetSRID(func.ST_MakePoint(longitude, 0), 4326),
        )
        database_session.add(reclamacao)
        i = 1 + 1
    database_session.commit()
    token = login("email_10@teste.com", "senha_10")
    response = client.get(
        "/reclamacoes-proximas",
        headers={"Authorization": f"Bearer {token}"},
        query_string={
            "latitude": "0",
            "longitude": "60",
            "page": "0",
            "categoria": "via",
        },
    )
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_reclamacoes_proximas_sem_reclamacoes(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.get(
        "/reclamacoes-proximas",
        headers={"Authorization": f"Bearer {token}"},
        query_string={
            "latitude": "0",
            "longitude": "61",
            "page": "0",
            "categoria": "lixo",
        },
    )
    assert response.status_code == 200
    assert len(response.json) == 0
