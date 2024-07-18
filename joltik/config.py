from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    environment: str = "dev"
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int = 5432

    google_client_id: str
    google_developer_token: str
    google_client_secret: str
    google_login_customer_id: str

    secret: str

    @property
    def postgres_url(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                path="testdb" if self.environment == "unittest" else self.postgres_db,
            ),
        )


config = Config()
