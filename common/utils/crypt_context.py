from passlib.context import CryptContext

crypto_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
