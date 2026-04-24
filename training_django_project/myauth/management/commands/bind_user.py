from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        user = User.objects.get(pk=6)
        group, created = Group.objects.get_or_create(
            name="profile_manager",
        )
        permission_profile = Permission.objects.get(
            codename="view_profile",
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry",
        )

        group.permissions.add(permission_profile)

        user.groups.add(group)

        user.user_permissions.add(permission_logentry)

        group.save()
        user.save()
        self.stdout.write(
            self.style.SUCCESS("Successfully bind user to groups and permissions")
        )
