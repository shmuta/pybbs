#django imports
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
#pybbs imports
from pybbs.bbs.models import Message
#python imports
from types import NoneType

from django.http import HttpResponse

def index(request):

    root = Message.objects.filter(title = 'root')
    latest_message_list = Message.objects.filter(parent=root).order_by('-post_date')[:5]
    index = loader.get_template('pybbs/index.html')
    c = Context({
        'latest_message_list': latest_message_list,
    })
    return HttpResponse(index.render(c))

def detail(request, message_id):
    m = get_object_or_404(Message, pk=message_id)
    reply_list = Message.objects.filter(parent=m)

    current_parent = m.parent
    parent_list = [current_parent]
    while ((not isinstance(current_parent, NoneType)) and (current_parent.title != 'root')):
        current_parent = current_parent.parent
        parent_list.insert(0, current_parent)
    return render_to_response('pybbs/detail.html', {
            'message': m,
            'parent_list': parent_list,
            'reply_list': reply_list,
            'user': request.user
            })

def reply(request, message_id):
    parent_message = get_object_or_404(Message, pk=message_id)
    if request.user.is_authenticated():
        try:
            title = request.POST['title']
        except (KeyError):
            # Redisplay the message detail form.
            return render_to_response('pybbs/detail.html', {
                'message': parent_message,
                'error_message': "You didn't specify a message title.",
            })
        #TODO: ekondrashev 16.08.09: Maybe there is a way to know what field is missing from
        #KeyError to avoid duplication of code, need to figure out
        try:
            message = request.POST['message']
        except (KeyError):
            # Redisplay the message detail form.
            return render_to_response('pybbs/detail.html', {
                'message': parent_message,
                'error_message': "You didn't specify a message text.",
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
