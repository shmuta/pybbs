#django imports
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

#pybbs imports
from pybbs.bbs.models import Message

#python imports
from types import NoneType

def _add_parents(parents, parent_list):
    if parents:
        parent_list.insert(0, parents)
    for current_parent in parents:
        _add_parents(current_parent.parents.all(), parent_list)
    return parent_list

def _list_messages(request, message_id=None, context=None):
    """Populates context with message replies"""
    message     = get_object_or_404(Message, pk=message_id)
    parent_list = _add_parents(message.parents.all(), parent_list = [])
    reply_list  = Message.objects.filter(parents=message_id)            \
                  .order_by('-post_date')
    ctxt_dict   = {'message': message,'parent_list': parent_list,       \
                   'reply_list': reply_list}
    context     = RequestContext(request, ctxt_dict) if context is None \
                  else context.update(ctxt_dict)
    return context

def _list_thems(request, context=None):
    """Populates context with thems messages"""
    thems     = Message.objects.filter(parents=None)                  \
                .order_by('-post_date')
    ctxt_dict = {'thems': thems} 
    context   = RequestContext(request, ctxt_dict) if context is None \
                else context.update(ctxt_dict)
    return context

def index(request, template='pybbs/index.html'):
    context = _list_thems(request)
    return render_to_response(template, {}, context)

def detail(request, message_id, template='pybbs/detail.html'):
    context = _list_messages(request, message_id)
    return render_to_response(template, {}, context)

def reply(request, message_id):
    parent_message = get_object_or_404(Message, pk=message_id)
    if request.user.is_authenticated():
        try:
            error_message = _("Error: not specified a message title.")
            title = request.POST['title']
            error_message = _("Error: not specified a message text.")
            body = request.POST['body']
        except (KeyError):
            # Redisplay the message detail form.
            return render_to_response('pybbs/detail.html', {
                'error_message': error_message,
            })
        else:
            new_message = Message(title=title, body=body, owner=request.user)
            new_message.save()
            new_message.parents.add (parent_message)
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('pybbs.bbs.views.detail', args=(message_id,)))
    else:
        return render_to_response('pybbs/detail.html', {
                'error_message': _("You are not logged in."),
            })
    
def create(request):
    if request.user.is_authenticated():
        try:
            error_message = _("Error: not specified a message title.")
            title = request.POST['title']
            error_message = _("Error: not specified a message text.")
            body = request.POST['body']
        except (KeyError):
            # Redisplay the message detail form.
            return render_to_response('pybbs/detail.html', {
                'error_message': error_message,
            })
        else:
            new_message = Message(title=title, body=body, owner=request.user)
            new_message.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('pybbs.bbs.views.detail', args=(new_message.id,)))
    else:
        return render_to_response('pybbs/detail.html', {
                'error_message': _("You are not logged in."),
            })

