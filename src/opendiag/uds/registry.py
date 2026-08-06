class ServiceRegistry:
    def __init__(self):
        self._services = {}

    def register(
        self,
        service_id: int,
        service,
    ):
        self._services[service_id] = service

    def get(
        self,
        service_id: int,
    ):
        return self._services[service_id]
