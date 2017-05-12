from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

_url = 'http://{}/'.format(settings.REST_SERVER_HOSTNAME)


@cache_page(30)
def index(request):
    return HttpResponse('''\
<html><head><title>Welcome to the Django workload!</title></head>
<body>
<H1>Welcome to the Django workload!</H1>
</body>
</html>''')
