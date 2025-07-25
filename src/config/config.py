from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    
    model_config = SettingsConfigDict(
        env_file="../.env", 
        extra="ignore",
        env_prefix=""  
    )

config = Settings()