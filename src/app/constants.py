from passlib.context import CryptContext

SECRET_KEY = "6fac9ddbcab53ed68cf3c577db8fb8de06d3b7b6f27c0c8ddb47a07460677c82"
ALGORITHEM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")