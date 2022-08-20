from pydantic import BaseSettings

class Settings(BaseSettings):
    db_hostname: str 
    db_username: str 
    db_password: str 
    db_name: str
    token_secret_key: str
    token_algorithm: str
    token_expiration_time_minutes: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()
