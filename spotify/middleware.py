from django.http.response import HttpResponseForbidden

def blacklist_middleware(get_response):
    def middleware(request):
        ip_address = request.META['REMOTE_ADDR']

        if ip_address not in ('127.0.0.12',):
            return HttpResponseForbidden()

        return get_response(request)

    return middleware


class BlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META['REMOTE_ADDR']

        if ip_address not in ('127.0.0.1',):
            return HttpResponseForbidden()

        return self.get_response(request)
