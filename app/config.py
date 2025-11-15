"""Application configuration"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    database_url: str = "postgresql+psycopg2://user:pass@localhost/Restaurant"

    # OpenAI
    openai_api_key: str = ""

    # LangChain
    langsmith_tracing: bool = True
    langsmith_api_key: str = ""
    langsmith_project: str = "Restaurant-copilot"
    langsmith_endpoint: str

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
