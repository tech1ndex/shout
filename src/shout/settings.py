from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str
    team_name: str
    victory_sound_path: str

    class Config:
        env_file = ".env"
