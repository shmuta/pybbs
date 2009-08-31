#django imports
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
#pybbs imports
from pybbs.bbs.models import Message
#python imports
from types import NoneType

from django.http import HttpResponse

def index(request):
    ''' Temporary render detail for root message '''
    try:
        root = Message.objects.filter(title = 'root')[0]
        return detail(request, root.id)
    except (LookupError):
        return render_to_response('pybbs/detail.html', {'error_message': "LookupError Error",})

def detail(request, message_id):
    message        = get_object_or_404(Message, pk=message_id)
    reply_list     = message.related_messages.all()
    current_parent = message.parent
    parent_list    = [current_parent]
    while (not isinstance(current_parent, NoneType)):
        current_parent = current_parent.parent
        parent_list.insert(0, current_parent)
    return render_to_response('pybbs/detail.html', {
            'message': message,
            'parent_list': parent_list,
            'reply_list': reply_list,
            'user': request.user
            })

def reply(request, message_id):
    parent_message = get_object_or_404(Message, pk=message_id)
    if request.user.is_authenticated():
        try:
            error_message = "Error: not specified a message title."
            title = request.POST['title']
            error_message = "Error: not specified a message text."
            message = request.POST['message']
        except (KeyError):
            # Redisplay the message detail form.
            return render_to_response('pybbs/detail.html', {
                'message': parent_message,
                'error_message': error_message,
            })
        else:
            new_message = Message(parent=parent_message, title=title, message=message, owner=request.user)
            new_message.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('pybbs.bbs.views.detail', args=(new_message.id,)))
    else:
        return render_to_response('pybbs/detail.html', {
                'message': parent_message,
                'error_message': "You are not logged in.",
            })
