from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Sales


@receiver(post_save, sender=Sales, dispatch_uid='my_handler')
def my_handler(**kwargs):
    instance = kwargs.get("instance")
    created = kwargs.get("created")
    print("It works")
    if created:
        instance.product.quantity -= instance.quantity
        instance.product.save()
    else:
        print("Update")


