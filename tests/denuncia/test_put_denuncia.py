def test_put_denuncia(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/denuncia?id=11",
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
            "status": "resolvido"
        },
    )
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "categoria",
        "cep",
        "criacao",
        "data",
        "descricao",
        "endereco",
        "fotos",
        "id",
        "latitude",
        "longitude",
        "numero_endereco",
        "ponto_referencia",
        "qtd_curtidas",
        "status"
    ]

def test_put_denuncia_nao_encontrada(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/denuncia?id=999",
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
    assert response.json == {"msg": "denuncia nao encontrada"}

def test_put_denuncia_sem_body(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/denuncia?id=11",
        headers={"Authorization": f"Bearer {token}"},
        json={}
    )
    assert response.status_code == 200
    assert response.json == {"msg": "nada foi alterado"}