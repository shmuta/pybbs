from django.template import Context, loader
from pybbs.bbs.models import Message

from django.http import HttpResponse

def index(request):

    latest_message_list = Message.objects.order_by('-post_date')[:5]
    t = loader.get_template('pybbs/index.html')
    c = Context({
        'latest_message_list': latest_message_list,
    })
    return HttpResponse(t.render(c))
