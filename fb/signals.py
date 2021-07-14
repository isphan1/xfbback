from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from fb.models import Profile,RelationShip
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=RelationShip)
def post_save_create_relationship(sender,instance,created,**kwargs):

    sender_ = instance.sender
    receiver_ = instance.receiver
    room = instance.room
    
    if instance.status == 'ACCPETED':
        room = get_random_string(8)
        # instance.room = get_random_string(8)
        sender_.friends.add(receiver_.profile)
        receiver_.friends.add(sender_.profile)
        sender_.save()
        receiver_.save()
