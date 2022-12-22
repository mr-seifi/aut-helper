import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from bot import main


class Command(BaseCommand):
    help = 'Starts telegram bot'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
        main()
