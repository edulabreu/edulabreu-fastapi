from passlib.context import CryptContext


password_cxt = CryptContext(schemes='bcrypt', deprecated='auto')  #Usando CryptContext para criptografar a senha

class Hash():
    def bcrypt(password: str):
        return password_cxt.hash(password)

    def verify(hashed_password, plain_password):  # Utilizar para Verificar o password se bate com o password criptografado
        return password_cxt.verify(plain_password, hashed_password)

