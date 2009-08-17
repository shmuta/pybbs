from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404

from pybbs.bbs.models import Message


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
    return render_to_response('pybbs/detail.html', {'message': m})

def reply(request, message_id):
    parent = get_object_or_404(Message, pk=message_id)
    try:
        title = request.POST['title']
    except (KeyError):
        # Redisplay the message detail form.
        return render_to_response('pybbs/detail.html', {
            'message': parent,
            'error_message': "You didn't specify a message title.",
        })
    #TODO: ekondrashev 16.08.09: Maybe there is a way to know what field is missing from
    #KeyError to avoid duplication of code, need to figure out
    try:
        message = request.POST['message']
    except (KeyError):
        # Redisplay the message detail form.
        return render_to_response('pybbs/detail.html', {
            'message': parent,
            'error_message': "You didn't specify a message text.",
        })
    else:
        new_message = Message(parent=parent, title=title, message=message)
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('mysite.polls.views.results', args=(p.id,)))
