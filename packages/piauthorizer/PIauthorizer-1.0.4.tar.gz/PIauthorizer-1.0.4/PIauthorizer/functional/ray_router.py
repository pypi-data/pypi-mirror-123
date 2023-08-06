import os
import sys

import ray
from fastapi import APIRouter
from PIauthorizer import ConfigManager
from PIauthorizer.logging.logged_route import LoggedRoute
from ray import serve
from ray.cluster_utils import Cluster

config_manager = ConfigManager()

ray_router = APIRouter(
    route_class=LoggedRoute, tags=['Ray'], dependencies=config_manager.get_dependencies()
)

@ray_router.on_event("startup")
def startup_event():
    if "pytest" in sys.modules or "--reload" in sys.argv:
        cluster = Cluster(
        initialize_head=True,
        head_node_args={
            "num_cpus": os.cpu_count(),
        })
        ray.init(address=cluster.address)
    else:
        head_service_ip = os.environ.get(f"NLP_CLUSTER_RAY_HEAD_SERVICE_HOST")
        client_port = os.environ.get("NLP_CLUSTER_RAY_HEAD_SERVICE_PORT_CLIENT")
        ray.util.connect(f"{head_service_ip}:{client_port}", ray_init_kwargs={'runtime_env':{'env_vars': dict(os.environ)}})
    assert ray.is_initialized() == True
    serve.start()

@ray_router.get('/delete')
def delete(name:str):
    serve.get_deploryment(name).delete()
    return 'ok'

@ray_router.get('/show_deployments')
def show_deployments():
    deployment_list = serve.list_deployments()
    deployment = {}
    for key, _ in deployment_list.items():
        info = deployment_list[key].ray_actor_options
        info['num_replicas'] = deployment_list[key].num_replicas
        info['init_args'] = deployment_list[key].init_args
        info['func_or_class'] = deployment_list[key].func_or_class.__name__
        deployment[key] = info
    return deployment

@ray_router.get('/update_deployment')
def update_deployment(name:str, num_replicas:int, num_cpus: float = 0.1, num_gpus: float = 0.0, memory_mb:int=100):
    serve.get_deployment(name).options(num_replicas=num_replicas, ray_actor_options={'num_cpus': num_cpus, 'num_gpus': num_gpus, 'memory': 1024*1024*memory_mb}).deploy()
    return 'ok'

@ray_router.get('/cluster_resources')
def cluster_resources(): 
    return ray.cluster_resources()

@ray_router.get('/available_resources')
def available_resources():
    return ray.available_resources()
    
@ray_router.on_event("shutdown")  # Code to be run when the server shutdown.
async def shutdown_event():
    for key in serve.list_deployments().keys():
        serve.get_deployment(key).delete()
    ray.shutdown()
