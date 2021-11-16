from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from src.helpers.jwt import InvalidTokenException, get_user_id_from_token


security = HTTPBearer()


async def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    token = credentials.credentials
    try:
        get_user_id_from_token(token)
    except InvalidTokenException as e:
        raise HTTPException(status_code=401, detail=str(e))


PROTECTED = [Depends(has_access)]
