from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = "Seed default users"

    def handle(self, *args, **kwargs):

        users = [
            {
                "email": "admin@parkingbus.com",
                "password": "Admin123!",
                "first_name": "System",
                "last_name": "Administrator",
                "is_active": True
            },
            {
                "email": "operator@parkingbus.com",
                "password": "Operator123!",
                "first_name": "Parking",
                "last_name": "Operator",
                
                "is_active": True
            },
            {
                "email": "user@parkingbus.com",
                "password": "User123!",
                "first_name": "Test",
                "last_name": "User",
                "is_active": True
            },
        ]

        for data in users:
            email = data["email"]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_active": data["is_active"],
                }
            )

            if created:
                user.set_password(data["password"])
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {email}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("User seeding completed.")
        )