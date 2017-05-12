import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from .users import require_user


@cache_page(30)
def index(request):
    return HttpResponse('''\
<html><head><title>Welcome to the Django workload!</title></head>
<body>
<h1>Welcome to the Django workload!</h1>

<p>The following views are being tested</p>

<dl>
<dt><a href="/feed_timeline">feed_timeline</a></dt>
<dd>A simple per-user feed of entries in time</dd>

</body>
</html>''')


@require_user
def feed_timeline(request):
    # Produce a JSON response containing the 'timeline' for a given user
    user = request.user
    feed = user.feed_entries().limit(20)
    user_info = {'name': user.name, 'pk': str(user.id)}
    result = {
        'num_results': len(feed),
        'items': [
            {'pk': str(e.id), 'comment_count': e.comment_count, 'user': user_info}
            for e in feed]
    }
    return HttpResponse(json.dumps(result), content_type='text/json')
