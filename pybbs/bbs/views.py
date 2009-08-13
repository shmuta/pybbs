from pybbs.bbs.models import Message
from django.http import HttpResponse

def index(request):
    latest_message_list = Message.objects.all().order_by('-post_date')[:5]
    output = ', '.join([message.name for message in latest_message_list])
    return HttpResponse(output)
