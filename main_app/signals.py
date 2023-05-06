from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from main_app.models import CustEnq,EnqDtl,Review
from django.conf import settings



@receiver(post_save, sender=CustEnq)
def create_profile(sender, instance, created, **kwargs):
    if created:
        EnqDtl.objects.create(enqno=instance)
        Review.objects.create(enqno=instance)


from django.contrib.auth.models import User



# @receiver(pre_save, sender=CustEnq)
# def checker(sender, instance, **kwargs):
#     if instance.id is None:
#         pass
#     else:
#         current=instance
#         previous=CustEnq.objects.last()
#         if previous.id!= current.id:
#             EnqDtl.objects.create(enqno=instance)
#             Review.objects.create(enqno=instance)
#

# @receiver(post_save, sender=EnqDtl)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         print("instance is ",instance)
#         print("instance.id is ", instance.id)
#         Review.objects.create(rspno=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()