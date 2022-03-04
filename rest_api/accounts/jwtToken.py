import jwt
from rest_framework.response import Response
from rest_framework import status

secret = "@#$!%^&*%()@#$%^!@(^&$"

def EncodeData(data):
    return jwt.encode(data, secret, algorithm="HS256")

def DecodeData(data):
    try:
        return jwt.decode(data, secret, algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError as e:
        return str(e)
    except jwt.exceptions.DecodeError as e:
        return str(e)
    except jwt.exceptions.InvalidKeyError as e:
        return str(e)
    except jwt.exceptions.InvalidTokenError as e:
        return str(e)