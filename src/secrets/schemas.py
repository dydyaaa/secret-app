from pydantic import BaseModel


class SecretCreate(BaseModel):
    secret: str
    passphrase: str | None = None
    ttl_seconds: int = 0
    
class SecretBase(BaseModel):
    unique_key: str
    
class Passphrase(BaseModel):
    passphrase: str | None = None
    
class SecretResponse(BaseModel):
    secret: str
    