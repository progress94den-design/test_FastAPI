from pathlib import Path
from pydantic import BaseModel, PostgresDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class RunServer(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class EmailConfig(BaseModel):
    host: str
    port: int
    # admin_email: str = "admin@site.com"
    admin_email: str


class TaskiqConfig(BaseModel):
    # url: AmqpDsn
    host: str
    port: int = 5672
    user: str
    password: str

    # amqp://guest:guest@localhost:5672//
    @property
    def url(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=f"/",
        )


class MinioConfig(BaseModel):
    host: str
    port: int = 9000
    # endpoint: str
    access_key: str
    secret_key: str
    secure: bool = False

    @property
    def endpoint(self) -> str:
        return f"{self.host}:{self.port}"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    auth: str = "/auth"
    article: str = "/article"
    category: str = "/category"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class CookieConfig(BaseModel):
    secret: str
    cookie_max_age: int = 3600
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: str
    name: str
    #
    # url: PostgresDsn

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # postgresql+asyncpg://us_api_db:pas_api_db@db:5432/api_db
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=f"{self.name}",
        )

    # Naming Conventions into Operations, Autogenerate
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=(BASE_DIR / ".env",),
    )
    run_server: RunServer = RunServer()
    api_prefix: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    cookie: CookieConfig
    email: EmailConfig
    taskiq: TaskiqConfig
    minio: MinioConfig


settings = Settings()
print(settings.db.url)
