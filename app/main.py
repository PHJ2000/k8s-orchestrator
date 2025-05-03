from fastapi import FastAPI, HTTPException
from app.k8s_manager import create_deployment, delete_deployment, get_status
from app.schemas import DeployRequest

app = FastAPI()

@app.post("/deploy")
def deploy_app(req: DeployRequest):
    try:
        create_deployment(req.name, req.image, req.port)
        return {"message": f"{req.name} deployed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{name}")
def status(name: str):
    return get_status(name)

@app.delete("/delete/{name}")
def delete_app(name: str):
    delete_deployment(name)
    return {"message": f"{name} deleted"}
