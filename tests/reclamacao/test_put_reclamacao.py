def test_put_reclamacao(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/reclamacao?id=11",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "descricao": "descricao teste",
            "data": "2024-09-25 23:13:00.000000",
            "endereco": "rua teste",
            "categoria": "lixo",
            "numero_endereco": "123",
            "ponto_referencia": "perto do teste",
            "cep": "12345-123",
            "bairro": "bairro teste",
            "cidade": "cidade teste",
            "estado": "AM",
            "latitude": "-1234567890",
            "longitude": "-1234567890",
            "status": "resolvido"
        },
    )
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "bairro",
        "categoria",
        "cep",
        "cidade",
        "criacao",
        "data",
        "descricao",
        "endereco",
        "estado",
        "fotos",
        "id",
        "latitude",
        "longitude",
        "numero_endereco",
        "ponto_referencia",
        "qtd_curtidas",
        "status",
    ]

def test_put_reclamacao_nao_encontrada(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/reclamacao?id=999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "descricao": "descricao teste",
            "data": "2024-09-25 23:13:00.000000",
            "endereco": "rua teste",
            "categoria": "lixo",
            "numero_endereco": "123",
            "ponto_referencia": "perto do teste",
            "cep": "12345-123",
            "latitude": "-1234567890",
            "longitude": "-1234567890",
        },
    )
    assert response.status_code == 404
    assert response.json == {"msg": "reclamacao nao encontrada"}

def test_put_reclamacao_sem_body(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/reclamacao?id=11",
        headers={"Authorization": f"Bearer {token}"},
        json={}
    )
    assert response.status_code == 200
    assert response.json == {"msg": "nada foi alterado"}