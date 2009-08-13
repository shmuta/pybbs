from django.db import models
from django.contrib.auth.models import User

class Label(models.Model):
    LABEL_TYPES = (
        (u'c1', u'label1'),
        (u'c2', u'label2'),
    )
    name = models.CharField(max_length=50, choices=LABEL_TYPES)
    def __unicode__(self):
        return self.name

class Message(models.Model):
    name = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
    post_date = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey('self', related_name='parent_message', null=True, blank=True)
    owner = models.ForeignKey(User, related_name="owner_user")

    def __unicode__(self):
        return self.post_date.ToString() + ' ' + self.message

class LabelList(models.Model):
    message = models.ForeignKey(Message)
    label = models.ForeignKey(Label)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.user + ' ' + self.label

class RatingList(models.Model):
    message = models.ForeignKey(Message)
    RATINGS = (
        (u'1', u'r1'),
        (u'2', u'r2'),
    )
    rating = models.CharField(max_length=10, choices=RATINGS)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.user + ' ' + self.rating

class Category(models.Model):
    CATEGORY_TYPES = (
        (u'c1', u'category1'),
        (u'c2', u'category2'),
    )
    name = models.CharField(max_length=50, choices=CATEGORY_TYPES)

    def __unicode__(self):
        return self.name



