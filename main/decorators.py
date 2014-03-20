from django.http import HttpResponseRedirect

def is_user_logged_in(function):
    def wrapper(request, *args, **kw):
        if not request.session.get('userId'):
            return HttpResponseRedirect('login')
        else:
            return function(request, *args, **kw)
    return wrapper