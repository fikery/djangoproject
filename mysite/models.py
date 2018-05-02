from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Poll(models.Model):
    name=models.CharField(max_length=200,null=False)
    created_at=models.DateField(auto_now_add=True)
    enabled=models.BooleanField(default=False)
    auther=models.CharField(max_length=100,default='佚名',editable=False)

    def __str__(self):
        return self.name

class PollItem(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=False)
    image_url=models.URLField(null=True,blank=True)
    vote=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class VoteCheck(models.Model):
    userid=models.PositiveIntegerField()
    pollid=models.PositiveIntegerField()
    voteDate=models.DateField()