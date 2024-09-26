import os


def test_carrega_variaveis_de_ambiente():
    assert os.environ["DB_URI"]
    assert os.environ["JWT_KEY"]
    assert os.environ["AZURE_CONNECTION_STRING"]
    assert os.environ["AZURE_BLOB_CONTAINER"]
    assert os.environ["AZURE_BLOB_URL"]
    assert os.environ["PORT"]


def test_endpoint_versao(client):
    response = client.get("/")
    assert (
        b"A aplica\xc3\xa7\xc3\xa3o est\xc3\xa1 rodando na vers\xc3\xa3o 1.7.0"
        in response.data
    )
