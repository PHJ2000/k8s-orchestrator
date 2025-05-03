from fastapi import FastAPI, HTTPException
from app.k8s_manager import create_deployment, delete_deployment, get_status, list_deployments
from app.schemas import DeployRequest, StatusResponse

app = FastAPI()

@app.post("/deploy")
def deploy_app(request: DeployRequest):
    create_deployment(name=request.name, image=request.image)
    return {"message": f"Deployment '{request.name}' with image '{request.image}' created successfully."}

@app.get("/status/{name}", response_model=StatusResponse)
def status(name: str):
    return get_status(name)

@app.delete("/delete/{name}")
def delete_app(name: str):
    delete_deployment(name)
    return {"message": f"{name} deleted"}

@app.get("/list")
def get_deployments():
    return list_deployments()
