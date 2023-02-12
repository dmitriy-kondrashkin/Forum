from django.http.response import HttpResponseRedirect


def start_redirect_view(request):
    return HttpResponseRedirect('/feed')