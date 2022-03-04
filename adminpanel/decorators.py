from django.shortcuts import redirect


def login_is_required(function):
    def wrapper(request, *args, **kw):
        if request.session.get('user') is None:
            return redirect('login')
        else:
            return function(request, *args, **kw)

    return wrapper
