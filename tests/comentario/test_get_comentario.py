def test_get_comentario(client):
    response = client.get("/comentario?reclamacao=1&page=0")
    assert response.status_code == 200
    for json in response.json:
        assert sorted(json.keys()) == [
            "criacao",
            "foto",
            "id_comenatario",
            "id_usuario",
            "nome",
            "texto",
        ]
