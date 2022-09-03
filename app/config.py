from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str 
    database_username: str 
    database_password: str 
    database_name: str
    token_secret_key: str
    token_algorithm: str
    token_expiration_time_minutes: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()
