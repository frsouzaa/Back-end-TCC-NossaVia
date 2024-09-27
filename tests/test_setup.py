import os
import re


def test_carrega_variaveis_de_ambiente():
    assert os.environ["DB_URI"]
    assert os.environ["JWT_KEY"]
    assert os.environ["AZURE_CONNECTION_STRING"]
    assert os.environ["AZURE_BLOB_CONTAINER_USUARIOS"]
    assert os.environ["AZURE_BLOB_CONTAINER_DENUNCIAS"]
    assert os.environ["AZURE_BLOB_URL"]
    assert os.environ["PORT"]


def test_endpoint_versao(client):
    response = client.get("/")
    res = re.match(r"^A aplicação está rodando na versão (0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$", response.data.decode())
    if not res:
        raise AssertionError("Versão não está no formato semântico")        
