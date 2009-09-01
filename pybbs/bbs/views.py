#python imports
from types import NoneType

#django imports
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

#pybbs imports
from pybbs.bbs.models import Message

def index(request):
    root_message_list = Message.objects.filter(parent=None).order_by('-post_date')
    index = loader.get_template('pybbs/index.html')
    c = Context({
        'root_message_list': root_message_list,
    })
    return HttpResponse(index.render(c))

def detail(request, message_id):
    message        = get_object_or_404(Message, pk=message_id)
    reply_list     = message.related_messages.all()
    current_parent = message.parent
    parent_list    = []
    while (not isinstance(current_parent, NoneType)):
        parent_list.insert(0, current_parent)
        current_parent = current_parent.parent
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
            body = request.POST['body']
        except (KeyError):
            # Redisplay the message detail form.
            return render_to_response('pybbs/detail.html', {
                'message': parent_message,
                'error_message': error_message,
            })
        else:
            new_message = Message(parent=parent_message, title=title, body=body, owner=request.user)
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
