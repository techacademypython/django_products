from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("It work")
        user = User.objects.get(id=1)
        for product in Product.objects.all():
            product.user = user
            product.save()
        print("Done !")
