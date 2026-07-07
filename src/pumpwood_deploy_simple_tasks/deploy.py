"""Kubernetes deployment manifests for Pumpwood simple task workers.

This module builds Secret and Deployment YAML files for RabbitMQ-backed
task containers. Manifests are registered with
``DeployPumpWood.add_microservice`` from ``pumpwood-deploy``.

Use ``PumpWoodSimpleTasksMicroservice`` when the task does not read
project storage. Use ``PumpWoodSimpleTasksWithStorageMicroservice`` when
the task must access cloud storage credentials from the cluster.
"""
import base64
from importlib import resources
from pumpwood_deploy.abc import BasePumpwoodDeployMicroservice
from pumpwood_deploy.type import (
    PumpwoodDeploy, PumpwoodDeployDeployment, PumpwoodDeploySecret)


secrets = resources.files('pumpwood_deploy_simple_tasks')\
    .joinpath('resources/secrets.yml')\
    .read_text(encoding='utf-8')
deploy_task = resources.files('pumpwood_deploy_simple_tasks')\
    .joinpath('resources/deploy__task.yml')\
    .read_text(encoding='utf-8')
deploy_task_storage = resources.files('pumpwood_deploy_simple_tasks')\
    .joinpath('resources/deploy__task_storage.yml')\
    .read_text(encoding='utf-8')


class PumpWoodSimpleTasksMicroservice(BasePumpwoodDeployMicroservice):
    """Deploy Kubernetes manifests for one simple task without storage.

    Renders a per-image Secret and Deployment for a RabbitMQ consumer
    task. Add one instance per task image that must run in the cluster.

    Example:
        ```python
        import os
        from pumpwood_deploy.deploy import DeployPumpWood
        from pumpwood_deploy_simple_tasks import (
            PumpWoodSimpleTasksMicroservice)

        deploy.add_microservice(
            PumpWoodSimpleTasksMicroservice(
                image="my-simple-task",
                version=os.getenv("MY_SIMPLE_TASK_VERSION"),
                microservice_username="microservice--my-task",
                microservice_password=secrets["microservice--my-task"],
            ))
        ```
    """

    def __init__(self,
                 image: str,
                 version: str,
                 microservice_username: str,
                 microservice_password: str,
                 repository: str = "gcr.io/repositorio-geral-170012",
                 replicas: int = 1,
                 requests_memory: str = "20Mi",
                 requests_cpu: str = "1m",
                 limits_memory: str = "512Mi",
                 limits_cpu: str = "500m"):
        """Initialize simple task deployment without storage access.

        Args:
            image (str):
                Docker image name of the task worker.
            version (str):
                Container image tag.
            microservice_username (str):
                Service username stored in the task Secret.
            microservice_password (str):
                Plain-text service password encoded into the task Secret.
            repository (str):
                Docker registry for the image. Defaults to
                ``gcr.io/repositorio-geral-170012``.
            replicas (int):
                Number of pod replicas. Defaults to ``1``.
            requests_memory (str):
                Memory request for pods. Defaults to ``20Mi``.
            requests_cpu (str):
                CPU request for pods. Defaults to ``1m``.
            limits_memory (str):
                Memory limit for pods. Defaults to ``512Mi``.
            limits_cpu (str):
                CPU limit for pods. Defaults to ``500m``.
        """
        self.repository = repository.rstrip("/")
        self.image = image
        self.version = version
        self.replicas = replicas
        self.requests_memory = requests_memory
        self.requests_cpu = requests_cpu
        self.limits_memory = limits_memory
        self.limits_cpu = limits_cpu
        self.microservice_username = microservice_username
        self._microservice_username = base64.b64encode(
            microservice_username.encode()).decode()
        self._microservice_password = base64.b64encode(
            microservice_password.encode()).decode()

    def create_deployment_file(self) -> list[PumpwoodDeploy]:
        """Build Kubernetes manifests for one simple task image.

        Returns:
            list[PumpwoodDeploy]:
                Secret ``pumpwood_simple_tasks__{image}__secrets`` and
                Deployment ``pumpwood_simple_tasks__{image}__deploy`` for
                ``pumpwood-task--{image}``.
        """
        secrets_yml_fmt = secrets.format(
            image=self.image,
            microservice_username=self._microservice_username,
            microservice_password=self._microservice_password)
        deploy_task_yml_fmt = deploy_task.format(
            repository=self.repository,
            image=self.image,
            version=self.version,
            replicas=self.replicas,
            requests_memory=self.requests_memory,
            requests_cpu=self.requests_cpu,
            limits_memory=self.limits_memory,
            limits_cpu=self.limits_cpu)
        name = 'pumpwood_simple_tasks__{image}'.format(image=self.image)

        return [
            PumpwoodDeploySecret(
                name=name + '__secrets', content=secrets_yml_fmt),
            PumpwoodDeployDeployment(
                name=name + '__deploy', content=deploy_task_yml_fmt),
        ]


class PumpWoodSimpleTasksWithStorageMicroservice(
        BasePumpwoodDeployMicroservice):
    """Deploy Kubernetes manifests for one simple task with storage access.

    Mounts cloud storage keys and injects bucket settings from the
    cluster ``storage`` ConfigMap. Prefer
    ``PumpWoodSimpleTasksMicroservice`` when storage access is not
    required, because this variant increases the pod credential surface.

    Example:
        ```python
        import os
        from pumpwood_deploy.deploy import DeployPumpWood
        from pumpwood_deploy_simple_tasks import (
            PumpWoodSimpleTasksWithStorageMicroservice)

        deploy.add_microservice(
            PumpWoodSimpleTasksWithStorageMicroservice(
                image="my-storage-task",
                version=os.getenv("MY_STORAGE_TASK_VERSION"),
                microservice_username="microservice--my-task",
                microservice_password=secrets["microservice--my-task"],
            ))
        ```
    """

    def __init__(self,
                 image: str,
                 version: str,
                 microservice_username: str,
                 microservice_password: str,
                 repository: str = "gcr.io/repositorio-geral-170012",
                 replicas: int = 1,
                 requests_memory: str = "20Mi",
                 requests_cpu: str = "1m",
                 limits_memory: str = "512Mi",
                 limits_cpu: str = "500m"):
        """Initialize simple task deployment with storage access.

        ``STORAGE_BUCKET_NAME`` and ``STORAGE_TYPE`` are read from the
        cluster ``storage`` ConfigMap at runtime, not from this class.

        Args:
            image (str):
                Docker image name of the task worker.
            version (str):
                Container image tag.
            microservice_username (str):
                Service username stored in the task Secret.
            microservice_password (str):
                Plain-text service password encoded into the task Secret.
            repository (str):
                Docker registry for the image. Defaults to
                ``gcr.io/repositorio-geral-170012``.
            replicas (int):
                Number of pod replicas. Defaults to ``1``.
            requests_memory (str):
                Memory request for pods. Defaults to ``20Mi``.
            requests_cpu (str):
                CPU request for pods. Defaults to ``1m``.
            limits_memory (str):
                Memory limit for pods. Defaults to ``512Mi``.
            limits_cpu (str):
                CPU limit for pods. Defaults to ``500m``.
        """
        self.repository = repository.rstrip("/")
        self.image = image
        self.version = version
        self.replicas = replicas
        self.requests_memory = requests_memory
        self.requests_cpu = requests_cpu
        self.limits_memory = limits_memory
        self.limits_cpu = limits_cpu
        self.microservice_username = microservice_username
        self._microservice_username = base64.b64encode(
            microservice_username.encode()).decode()
        self._microservice_password = base64.b64encode(
            microservice_password.encode()).decode()

    def create_deployment_file(self) -> list[PumpwoodDeploy]:
        """Build Kubernetes manifests for one storage-enabled task image.

        Returns:
            list[PumpwoodDeploy]:
                Secret ``pumpwood_simple_tasks_storage__{image}__secrets``
                and Deployment
                ``pumpwood_simple_tasks_storage__{image}__deploy`` for
                ``pumpwood-task--{image}``.
        """
        secrets_yml_fmt = secrets.format(
            image=self.image,
            microservice_username=self._microservice_username,
            microservice_password=self._microservice_password)
        deploy_task_yml_fmt = deploy_task_storage.format(
            repository=self.repository,
            image=self.image,
            version=self.version,
            replicas=self.replicas,
            requests_memory=self.requests_memory,
            requests_cpu=self.requests_cpu,
            limits_memory=self.limits_memory,
            limits_cpu=self.limits_cpu)
        name = 'pumpwood_simple_tasks_storage__{image}'.format(
            image=self.image)

        return [
            PumpwoodDeploySecret(
                name=name + '__secrets', content=secrets_yml_fmt),
            PumpwoodDeployDeployment(
                name=name + '__deploy', content=deploy_task_yml_fmt),
        ]
