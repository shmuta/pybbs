# coding=UTF-8
#python imports
import os
import sys

#django imports
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

#pybbs imports
from bbs.models import Category
from bbs.models import Rating
from bbs.models import Label

CATEGORIES=(
        'Спорт',
        'Юмор',
        'Программирование',
        'Музыка',
        'Кино',
        'Книги',
        'Жизнь',
    )
RATINGS=(
        '1',
        '2',
        '3',
        '4',
        '5',
)
LABELS=(
        'label1',
        'label2',
)
if __name__ == "__main__":
    if os.path.exists(settings.DATABASE_NAME):
        print "Removing " + settings.DATABASE_NAME
	os.remove(settings.DATABASE_NAME)
    sys.argv.append("syncdb")

    execute_manager(settings)
    print "Creating categories"
    for category_name in CATEGORIES:
        category = Category(name=category_name)
        category.save();
    print Category.objects.all()

    print "Creating ratings"
    for rating_value in RATINGS:
        rating = Rating(value=rating_value)
        rating.save();
    print Rating.objects.all()

    print "Creating labels"
    for label_name in LABELS:
        label = Label(name=label_name)
        label.save();
    print Label.objects.all()
