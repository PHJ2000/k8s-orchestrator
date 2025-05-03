from pydantic import BaseModel

class DeployRequest(BaseModel):
    name: str
    image: str

class StatusResponse(BaseModel):
    name: str
    replicas: int
    available_replicas: int