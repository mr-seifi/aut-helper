from prometheus_client import start_http_server
from prometheus_client.metrics import Gauge
from .collector_service import CollectorService


class PrometheusService:

    def __init__(self):
        self._student_number = Gauge(
            'students_count',
            'Count of students signed in bot per hour'
        )

        self._trxs_number = Gauge(
            'trxs_count',
            'Count of transactions signed per hour'
        )

    def send(self):
        collector_service = CollectorService()
        self._student_number.set(
            collector_service.collect_unique_student_within_hour()
        )
        self._trxs_number.set(
            collector_service.collect_unique_trxs_within_hour()
        )

    @staticmethod
    def runserver(port=8000):
        start_http_server(port)
