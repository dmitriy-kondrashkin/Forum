from django.shortcuts import redirect

def user_is_not_authenticated(function=None, redirect_url='/feed'):
    def decorator(func):
        def _wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return func(request, *args, **kwargs)
        return _wrapper    
    if function:
        return decorator(function)
    return decorator