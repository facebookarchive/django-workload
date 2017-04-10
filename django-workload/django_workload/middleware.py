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
