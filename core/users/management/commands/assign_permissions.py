from django.core.management.base import BaseCommand
from users.permissions import assign_all_permissions

class Command(BaseCommand):
    help = 'Assign permissions to groups'

    def handle(self, *args, **kwargs):
        assign_all_permissions()
        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions to groups'))