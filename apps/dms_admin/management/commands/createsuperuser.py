from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.user.choices import UserRoleChoices
from dms.settings import ADMIN_USERNAME, ADMIN_PASSWORD

User = get_user_model()


class Command(BaseCommand):
    help = 'Create an admin (superuser) account'

    def handle(self, *args, **options):
        username = ADMIN_USERNAME

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Admin user already exists."))
            return

        User.objects.create_superuser(
            username=username,
            role=UserRoleChoices.admin,
            password=ADMIN_PASSWORD
        )

        self.stdout.write(self.style.SUCCESS("Admin user created successfully."))
