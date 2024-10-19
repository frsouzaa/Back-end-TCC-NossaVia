def test_post_usuario(client):
    response = client.post(
        "/usuario",
        json={
            "email": "usuario_cadastrado_1@email.com.br",
            "senha": "teste_usuario_cadastrado",
            "nome": "usuario",
            "cpf": "000.000.000-00",
            "endereco": "rua",
            "cep": "00000-000",
            "numero_endereco": "0",
            "complemento_endereco": "",
            "bairro": "bairro teste",
            "cidade": "cidade teste",
            "estado": "SP",
            "data_nascimento": "2004-06-15 00:00:00.000000",
            "sexo": "m",
            "telefone": "11 11111-1111",
        },
    )
    assert response.json == {"msg": "criado"}
    assert response.status_code == 201


def test_post_usuario_email_ja_cadastrado(client):
    payload = {
        "email": "test_cadastrar_usuario_email_ja_cadastrado2@email.com.br",
        "senha": "teste_usuario_cadastrado",
        "nome": "usuario",
        "cpf": "111.000.000-00",
        "endereco": "rua",
        "cep": "00000-000",
        "numero_endereco": "0",
        "complemento_endereco": "",
        "bairro": "bairro teste",
        "cidade": "cidade teste",
        "estado": "SP",
        "data_nascimento": "2004-06-15 00:00:00.000000",
        "sexo": "m",
        "telefone": "11 11111-1111",
    }
    response = client.post(
        "/usuario",
        json=payload,
    )
    assert response.status_code == 201
    payload["cpf"] = "111.222.000-00"
    response = client.post(
        "/usuario",
        json=payload,
    )
    assert response.status_code == 409
    assert response.json == {"msg": "email ja cadastrado"}


def test_post_usuario_cpf_ja_cadastrado(client):
    payload = {
        "email": "test_cadastrar_usuario_cpf_ja_cadastrado1@email.com.br",
        "senha": "teste_usuario_cadastrado",
        "nome": "usuario",
        "cpf": "999.000.000-00",
        "endereco": "rua",
        "cep": "00000-000",
        "numero_endereco": "0",
        "complemento_endereco": "",
        "bairro": "bairro teste",
        "cidade": "cidade teste",
        "estado": "SP",
        "data_nascimento": "2004-06-15 00:00:00.000000",
        "sexo": "m",
        "telefone": "11 11111-1111",
    }
    response = client.post(
        "/usuario",
        json=payload,
    )
    assert response.status_code == 201
    payload["email"] = "test_cadastrar_usuario_cpf_ja_cadastrado2@email.com.br"
    response = client.post(
        "/usuario",
        json=payload,
    )
    assert response.status_code == 409
    assert response.json == {"msg": "cpf ja cadastrado"}


def test_post_usuario_sexo_invalido(client):
    response = client.post(
        "/usuario",
        json={
            "email": "usuario_cadastrado_2@email.com.br",
            "senha": "teste_usuario_cadastrado",
            "nome": "usuario",
            "cpf": "000.333.000-00",
            "endereco": "rua",
            "cep": "00000-000",
            "numero_endereco": "0",
            "complemento_endereco": "",
            "bairro": "bairro teste",
            "cidade": "cidade teste",
            "estado": "SP",
            "data_nascimento": "2004-06-15 00:00:00.000000",
            "sexo": "a",
            "telefone": "11 11111-1111",
        },
    )
    assert response.status_code == 409
    assert response.json == {"msg": "sexo invalido"}


def test_post_usuario_sem_body(client):
    response = client.post(
        "/usuario",
        json={},
    )
    assert response.status_code == 400
    assert response.json == {
        "msg": {
            "cep": [
                "required field",
            ],
            "data_nascimento": [
                "required field",
            ],
            "email": [
                "required field",
            ],
            "endereco": [
                "required field",
            ],
            "nome": [
                "required field",
            ],
            "senha": [
                "required field",
            ],
            "sexo": [
                "required field",
            ],
            "telefone": [
                "required field",
            ],
            "cpf": [
                "required field",
            ],
            "bairro": [
                "required field",
            ],
            "cidade": [
                "required field",
            ],
            "estado": [
                "required field",
            ],
        },
    }
