import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until db is available"""

    def handle(self, *args, **options):
        self.stdout.write('waiting for db...')
        db_connection = None
        while not db_connection:
            try:
                # try to connect to DB
                db_connection = connections['default']
            except OperationalError:
                # if can't connect, wait for 1s
                self.stdout.write('DB unavailable, waiting 1 sec...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('DB available.'))
