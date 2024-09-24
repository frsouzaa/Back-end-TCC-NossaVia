def test_login_autorizado(client, seed):
    response = client.post(
        "/login", json={"email": "email_0@teste.com", "senha": "senha_0"}
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
        "token",
    ]


def test_login_nao_autorizado(client, seed):
    response = client.post(
        "/login", json={"email": "email_0@teste.com", "senha": "senha_errada"}
    )
    assert response.status_code == 401
    assert response.json == {"msg": "usuário ou senha incorretos"}
