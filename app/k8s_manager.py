from kubernetes import client, config
from jinja2 import Template
import yaml

config.load_kube_config()  # Minikube 기준

def create_deployment(name, image, port):
    with open("templates/deployment.yaml") as f:
        tpl = Template(f.read())
    rendered = tpl.render(name=name, image=image, port=port)
    obj = yaml.safe_load(rendered)

    apps_v1 = client.AppsV1Api()
    apps_v1.create_namespaced_deployment(namespace="default", body=obj)

def delete_deployment(name):
    apps_v1 = client.AppsV1Api()
    apps_v1.delete_namespaced_deployment(name=name, namespace="default")

def get_status(name):
    apps_v1 = client.AppsV1Api()
    dep = apps_v1.read_namespaced_deployment(name=name, namespace="default")
    return {
        "replicas": dep.status.replicas,
        "available": dep.status.available_replicas
    }
