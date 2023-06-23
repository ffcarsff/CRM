from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


# Create your models here.
class user(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_aagent = models.BooleanField(default=False)
class userporfile(models.Model):
    user = models.OneToOneField(user,on_delete=models.CASCADE,related_name='profile')
    def __str__(self):
        return self.user.username

class worker(models.Model):
    name = models.CharField(max_length=20)
    phone = models.IntegerField(default=0)
    email = models.EmailField()
    addr = models.TextField()
    comment = models.TextField()
    phonned = models.BooleanField(default=False)
    organisation = models.ForeignKey(userporfile,null=True,on_delete=models.SET_NULL)
    agent = models.ForeignKey('agent',null=True,blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name

class agent(models.Model):
    user = models.OneToOneField(user,on_delete=models.CASCADE)
    Task_Completion = models.BooleanField(default=False)
    organisation = models.ForeignKey(userporfile,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email
def post_user_created_signal(sender,instance,created,**kwargs):
    print(instance,created)
    if created:
        userporfile.objects.create(user=instance)
post_save.connect(post_user_created_signal,sender=user)