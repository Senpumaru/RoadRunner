from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Road Runner - IoT Data Synthesizer"
    KAFKA_BOOTSTRAP_SERVERS: str

    class Config:
        env_file = ".env"

settings = Settings()