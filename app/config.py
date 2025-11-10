"""Application configuration"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    database_url: str = "postgresql+psycopg2://user:pass@localhost/Restaurant"

    # OpenAI
    openai_api_key: str = ""

    # LangChain
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "Restaurant-copilot"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
