from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RunServer(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000

class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    run_server: RunServer = RunServer()
    api_prefix: ApiPrefix = ApiPrefix()

settings = Settings()
