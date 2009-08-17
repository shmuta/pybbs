from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=200)
    post_date = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey('self', related_name='parent_message', null=True, blank=True)
    owner = models.ForeignKey(User, related_name="owner_user")

    def __unicode__(self):
        # wanted to add post_date field, but didn't found how to get string representation.
        return self.title

class Label(models.Model):
    LABEL_TYPES = (
        (u'c1', u'label1'),
        (u'c2', u'label2'),
    )
    name = models.CharField(max_length=50, choices=LABEL_TYPES)

    def __unicode__(self):
        return self.name

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
        return self.user.username + ' ' + self.rating

class CategoryList(models.Model):
    CATEGORIES = (
        (u'root', u'Root category'),
        (u'c1', u'test category1'),
        (u'c2', u'test category2'),
        (u'c3', u'test category3'),
        (u'c4', u'test category4'),
    )
    category = models.CharField(max_length=50, choices=CATEGORIES)
    message = models.ForeignKey(Message)

    def __unicode__(self):
        return self.message + ' ' + self.category