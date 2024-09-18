# Nossa Via
Back-end do TCC de Análise e Desenvolvimento de Sistemas da FATEC Ipiranga. O projeto consiste em um aplicativo mobile Android para publicação de denúnicas de problemas em vias públicas, como por exemplo buracos e falta de sinalização. 

Para mais detalhes sobre a documentação visitar [Documentacao-TCC-NossaVia](https://github.com/frsouzaa/Documentacao-TCC-NossaVia).

## Recomendações
- Utilizar a versão `3.12.5` do Python
- Criar um virtualenv para a instalação das dependências

## Dependências

- Instalar as dependências com o comando: 
```shell
pip install -r requirements.txt
```

### Adicionar no arquivo `.env`

| Nome da variável        | Função  |
|-------------------------|---------|
| `DB_URI`                  | URI de conexão com o banco de dados |
| `JWT_KEY`                 | Chave para geração e validação de JWT |
| `AZURE_CONNECTION_STRING` | String de conexão da Azure |
| `AZURE_BLOB_CONTAINER`    | Nome do blob container |
| `AZURE_BLOB_URL`          | Link do blob container |
| `PORT`                    | Porta em que a aplicaçã vai rodar |

## Rodar o projeto

- Iniciar a aplicação com o comando:
```shell
python app.py
```

## CI/CD

Essa aplicação conta com uma esteira de CI/CD configurada em um GitHub Workflow localizado no arquivo `./github/workflows/cicd.yml`. Essa esteira é responsável por realizar build e push da imagem da Docker e o deploy em um Azure Container APP, e possui as seguintes condições de execução:

- O build só é feito caso a TAG contida no arquivo `image.json` não exista no repositório do projeto no DockerHub
- O push só é feito caso o build seja execultado com sucesso
- O deploy do container só é feito caso o push seja execultado com sucesso

## Banco de dados

Esse projeto conta com a bliblioteca alembic para versionar os schemas das tabelas do banco de dados.

- Para gerar uma nova migration: 
```shell
alembic revision --autogenerate -m "<DESCRICAO_MIGATION>"
```
- Para persistir as mudanças de uma nova migration no banco de dados configurado no arquivo .env:
```shell
alembic upgrade head
```

## Comando útil para manter a legibilidade do código de acordo com o [PEP8](https://peps.python.org/pep-0008/)

```shell
autopep8 --in-place --aggressive --recursive --exclude="./<NOME_DO_VIRTUALENV>/*" .
```