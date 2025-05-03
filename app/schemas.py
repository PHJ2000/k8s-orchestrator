from pydantic import BaseModel

class DeployRequest(BaseModel):
    name: str
    image: str
    port: int
