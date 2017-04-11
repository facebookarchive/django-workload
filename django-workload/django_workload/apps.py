from django.apps import AppConfig
from . import patches


class DjangoWorkloadConfig(AppConfig):
    name = 'django_workload'
    verbose = 'Django Workload'

    def ready(self):
        patches.apply()
