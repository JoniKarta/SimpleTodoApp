from datetime import datetime, timezone, timedelta

from jose import jwt

from configuration.config import Config

config = Config()


def create_access_token(data: dict, expire_min: int = 30) -> str:
    """
    Generates a JWT access token with the given data and expiration time.

    Args:
        data (dict): The payload data to be included in the JWT token.
        expire_min (int, optional): The expiration time in minutes. Defaults to 30 minutes.

    Returns:
        str: The encoded JWT access token as a string.


    Example:
        token = create_access_token({"sub": "user_id"})
    """

    claims = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=expire_min)
    claims.update({'exp': expire_time})
    return jwt.encode(claims, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodes a JWT access token and returns the payload data.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload data from the JWT token.

    Example:
        payload = decode_access_token("jwt_token_string")
    """

    return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
