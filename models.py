from pydantic import BaseModel

class Settings(BaseModel):
    version: str
    nick: str
    enable_resource: bool
    enable_custom_settings: bool