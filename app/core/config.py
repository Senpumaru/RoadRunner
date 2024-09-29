from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Road Runner - IoT Data Synthesizer"
    KAFKA_BOOTSTRAP_SERVERS: str
    DATABASE_URL: str = "postgresql+asyncpg://roadrunner:roadrunner_password@postgres:5432/roadrunner"
    # SECRET_KEY: str = "your-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()