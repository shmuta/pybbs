from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    title     = models.CharField(max_length=50)
    body      = models.TextField(max_length=200)
    post_date = models.DateTimeField(auto_now=True)
    parents   = models.ManyToManyField('self', related_name='related_messages', symmetrical=False, null=True, blank=True)
    owner     = models.ForeignKey( User,  related_name='pybbs_message_set')

    def __unicode__(self):
        # wanted to add post_date field, but didn't found how to get string representation.
        return self.title

class Label(models.Model):
    name      = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class LabelList(models.Model):
    message   = models.ForeignKey(Message)
    label     = models.ForeignKey(Label)
    user      = models.ForeignKey(User)

    def __unicode__(self):
        return self.user + ' ' + self.label

class RatingList(models.Model):
    message   = models.ForeignKey(Message)
    rating    = models.CharField(max_length=10)
    user      = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username + ' ' + self.rating

class CategoryList(models.Model):
    category  = models.CharField(max_length=50)
    message   = models.ForeignKey(Message)

    def __unicode__(self):
        return self.message + ' ' + self.category
