from django.utils.deprecation import MiddlewareMixin
from django_statsd.middleware import (
    GraphiteMiddleware,
    GraphiteRequestTimingMiddleware,
)


# Update django_statsd middleware to newer Django requirements
class GraphiteMiddleware(MiddlewareMixin, GraphiteMiddleware):
    pass


class GraphiteRequestTimingMiddleware(
        MiddlewareMixin, GraphiteRequestTimingMiddleware):
    pass


# We need access to request metadata from within patched support code. Store
# the request in a thread global
def global_request_middleware(get_response):
    from .global_request import ThreadLocalRequest

    def middleware(request):
        with ThreadLocalRequest(request):
            return get_response(request)

    return middleware
