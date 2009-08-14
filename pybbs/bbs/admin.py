from pybbs.bbs.models import RatingList
from pybbs.bbs.models import Message
from pybbs.bbs.models import LabelList
from pybbs.bbs.models import CategoryList
from pybbs.bbs.models import Label

from django.contrib import admin

admin.site.register(Message)
admin.site.register(Label)
admin.site.register(CategoryList)
admin.site.register(LabelList)
admin.site.register(RatingList)