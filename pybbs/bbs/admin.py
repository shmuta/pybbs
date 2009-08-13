from bbs_site.bbs.models import RatingList
from bbs_site.bbs.models import Message
from bbs_site.bbs.models import LabelList
from bbs_site.bbs.models import Category
from bbs_site.bbs.models import Label

from django.contrib import admin

admin.site.register(Message)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(LabelList)
admin.site.register(RatingList)