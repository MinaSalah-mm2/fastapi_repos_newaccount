
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# this hash function to hashing the coming password, different from the encryption as, the hashing 
# is a one way to apply modification on the data where can not return back the hashed data into 
# original data as coming, which differnce form the encryption where can encrypt/decrypt. 


def hash(password: str):
    return pwd_context.hash(password)

def verify(plainPassword, hashedPassword): 
    return pwd_context.verify(plainPassword, hashedPassword)