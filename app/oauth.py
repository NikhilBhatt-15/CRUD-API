from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone



#SECRET KEy
#ALGORITHM
# EXPIRATION TIME

SECRET_KEY = "8e3f3920d01400475fa80e2e68d6ac0b61a0777de563283c9c9299016c9f09cc"
ALGORTITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_tokes(data:dict,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_jwt =jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORTITHM)
    return encoded_jwt