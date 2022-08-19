from passlib.context import CryptContext

# We are using the BCrypt hashing algorithm. We are telling passlib to use it.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return  pwd_context.hash(password)