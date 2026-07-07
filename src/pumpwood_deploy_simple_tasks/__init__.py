"""Kubernetes deployment package for Pumpwood simple task workers.

Use ``PumpWoodSimpleTasksMicroservice`` or
``PumpWoodSimpleTasksWithStorageMicroservice`` with ``DeployPumpWood``
from ``pumpwood-deploy`` to generate and apply task worker manifests.

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

Add one microservice instance per task image. Tasks consume RabbitMQ
messages using credentials from ``general-secrets`` and
``rabbitmq-main-secrets`` deployed by ``StandardMicroservices``.
"""
from .deploy import (
    PumpWoodSimpleTasksMicroservice,
    PumpWoodSimpleTasksWithStorageMicroservice)

__all__ = [
    PumpWoodSimpleTasksMicroservice,
    PumpWoodSimpleTasksWithStorageMicroservice,
]
