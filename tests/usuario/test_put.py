def test_put(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/usuario",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "usuario",
            "endereco": "rua",
            "cep": "00000-000",
            "numero_endereco": "0",
            "complemento_endereco": "",
            "data_nascimento": "2004-06-15 00:00:00.000000",
            "sexo": "m",
            "telefone": "11 11111-1111",
        },
    )
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "cep",
        "complemento_endereco",
        "data_nascimento",
        "email",
        "endereco",
        "foto",
        "nome",
        "numero_endereco",
        "pontucao",
        "sexo",
        "telefone",
    ]


def test_put_sem_body(client, login):
    token = login("email_10@teste.com", "senha_10")
    response = client.put(
        "/usuario",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )
    assert response.status_code == 200
    assert response.json == {"msg": "nada foi alterado"}
