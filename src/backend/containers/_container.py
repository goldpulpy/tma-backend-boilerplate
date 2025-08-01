"""DI containers."""

from dependency_injector import containers, providers

from backend.containers.use_cases import ServiceUseCaseContainer
from backend.containers.user.use_cases import UserUseCaseContainer


class Container(containers.DeclarativeContainer):
    """Main DI container."""

    service_use_case = providers.Container(ServiceUseCaseContainer)

    user_use_case = providers.Container(UserUseCaseContainer)
