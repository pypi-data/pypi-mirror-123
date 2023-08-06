from pydantic import BaseSettings


class Configuration(BaseSettings):
    doc_username: str
    doc_password: str

    class Config:
        env_prefix = 'API_'  # defaults to no prefix, i.e. ""


conf = Configuration()
