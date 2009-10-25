#django imports
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, views as auth_views

#pybbs imports
from pybbs.bbs.models import Message, Theme, Category

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
    thems     = Theme.objects.all().order_by('-post_date')
    ctgr_list = Category.objects.all().order_by('-name')
    ctxt_dict = {'thems': thems, "category_list": ctgr_list} 
    context   = RequestContext(request, ctxt_dict) if context is None \
                else context.update(ctxt_dict)
    return context

def index(request, template='pybbs/index.html'):
    context = _list_thems(request)
    return render_to_response(template, {}, context)

def detail(request, message_id, template='pybbs/detail.html'):
    context = _list_messages(request, message_id)
    return render_to_response(template, {}, context)

def rss(request,template='rss.xml',context=None):
    message_list = Message.objects.all().order_by('-post_date')[:7]
    ctxt_dict = {'host': request.get_host(), 'message_list': message_list} 
    context   = RequestContext(request, ctxt_dict) if context is None \
                else context.update(ctxt_dict)
    return render_to_response(template, {}, context, mimetype="application/xml")

def rss_by_id(request,message_id,template='rss.xml',context=None):
    message_list = Message.objects.filter(parents=message_id).order_by('-post_date')[:7]
    ctxt_dict = {'host': request.get_host(), 'message_list': message_list}
    context   = RequestContext(request, ctxt_dict) if context is None \
                else context.update(ctxt_dict)
    return render_to_response(template, {}, context, mimetype="application/xml")

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
            # TODO: replace this with rendering error.html template
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
        # TODO: replace this with rendering error.html template
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
            # TODO: replace this with rendering error.html template
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
        # TODO: replace this with rendering error.html template
        return render_to_response('pybbs/detail.html', {
                'error_message': _("You are not logged in."),
            })

def create_theme(request):
    ctgrs = []
    if request.user.is_authenticated():
        try:
            error_message = _("Error: not specified a message title.")
            title = request.POST['title']
            error_message = _("Error: not specified a message text.")
            body = request.POST['body']
            error_message = _("Error: not specified categories list.")
            categories = request.POST.getlist('categories')
            for category_id in categories:
                ctgrs.append(get_object_or_404(Category, pk=category_id))
            if not ctgrs:
                raise KeyError
        except (KeyError):
            # Redisplay the message detail form.
            # TODO: replace this with rendering error.html template
            return render_to_response('pybbs/detail.html', {
                'error_message': error_message,
            })
        else:
            new_theme = Theme(title=title, body=body, owner=request.user)
            new_theme.save()
            for category in ctgrs:
                new_theme.categorys.add(category)
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('pybbs.bbs.views.detail', args=(new_theme.id,)))
    else:
        # TODO: replace this with rendering error.html template
        return render_to_response('pybbs/detail.html', {
                'error_message': _("You are not logged in."),
            })
			

def logout_user(request):
    lang_code = request.session['django_language']
    logout(request)
    if(lang_code):
	    request.session['django_language'] = lang_code
    return HttpResponseRedirect(request.GET.get('url', '/'))
	
def login_user(request):
    auth_views.login(request)    
    return HttpResponseRedirect(request.GET.get('url', '/'))

			
			