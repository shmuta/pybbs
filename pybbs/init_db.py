# coding=UTF-8

#python imports
import os

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

#Be sure to set utf-8 encoding at server side
#For MySQL, for example, add the following lines to my.cnf file:
#[mysqld]
#default-character-set=utf8
#skip-character-set-client-handshake
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

SQLITE_DB_ENGINE="sqlite3"

if __name__ == "__main__":
    if settings.DATABASE_ENGINE == SQLITE_DB_ENGINE and os.path.exists(settings.DATABASE_NAME):
        print "Removing " + settings.DATABASE_NAME
        os.remove(settings.DATABASE_NAME)
    else:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("drop database if exists %s; create database %s;" % (settings.DATABASE_NAME, settings.DATABASE_NAME))

    execute_manager(settings, ["","syncdb"])
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
