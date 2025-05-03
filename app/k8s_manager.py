from kubernetes import client, config
from jinja2 import Template
from app.schemas import StatusResponse
import yaml

config.load_kube_config()  # Minikube 기준
apps_v1 = client.AppsV1Api()
def create_deployment(name: str, image: str):
    apps_v1 = client.AppsV1Api()

    container = client.V1Container(
        name=name,
        image=image,
        ports=[client.V1ContainerPort(container_port=80)]
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container])
    )

    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={"matchLabels": {"app": name}}
    )

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )

    apps_v1.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )

def delete_deployment(name):
    apps_v1 = client.AppsV1Api()
    apps_v1.delete_namespaced_deployment(name=name, namespace="default")

def get_status(name: str) -> StatusResponse:
    dep = apps_v1.read_namespaced_deployment(name=name, namespace="default")
    return StatusResponse(
        name=dep.metadata.name,
        replicas=dep.status.replicas or 0,
        available_replicas=dep.status.available_replicas or 0,
    )
