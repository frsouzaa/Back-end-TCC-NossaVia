import bcrypt


def criptografar(senha: str) -> str:
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha.encode("utf-8"), salt)
    return hash_senha.decode("utf-8")


def descriptografar(senha: str, hash_senha: str):
    return bcrypt.checkpw(senha.encode("utf-8"), hash_senha.encode("utf-8"))
