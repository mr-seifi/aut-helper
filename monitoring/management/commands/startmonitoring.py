from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.services import PrometheusService
from time import sleep


class Command(BaseCommand):
    help = 'Starts monitoring service'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        prometheus_service = PrometheusService()
        prometheus_service.runserver()

        while True:
            prometheus_service.send()

            time = timezone.now().strftime('%X')
            self.stdout.write("%s -- Data fetched!" % time)
            sleep(60)
