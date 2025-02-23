from passlib.context import CryptContext

def get_hashing_tool() -> CryptContext:
    return CryptContext(
        schemes=["bcrypt"], deprecated="auto"
    )