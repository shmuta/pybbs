from pybbs.bbs.models import RatingList
from pybbs.bbs.models import Message
from pybbs.bbs.models import LabelList
from pybbs.bbs.models import Category
from pybbs.bbs.models import Label

from django.contrib import admin

admin.site.register(Message)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(LabelList)
admin.site.register(RatingList)