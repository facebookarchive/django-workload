import json
import random
import uuid

from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django_statsd.clients import statsd

from cassandra.cqlengine.query import BatchQuery

from .users import require_user
from .feed import Feed
from .models import BundleSeenModel


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

<dt><a href="/timeline">timeline</a></dt>
<dd>A ranked feed of entries from other users</dd>
</dl>

<dt>/seen (POST only endpoint)</dt>
<dd>A view to increase counters and last-seen timestamps</dd>

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
            {
                'pk': str(e.id),
                'comment_count': e.comment_count,
                'published': e.published.timestamp(),
                'user': user_info
            }
            for e in feed]
    }
    return HttpResponse(json.dumps(result), content_type='text/json')


@require_user
def timeline(request):
    # Produce a JSON response containing the feed of entries for a user
    feed = Feed(request)
    result = feed.feed_page()
    return HttpResponse(json.dumps(result), content_type='text/json')


@require_http_methods(['POST'])
@require_user
def seen(request):
    # For workload purposes we ignore the posted data, and instead generate
    # some random data of our own, cached in memcached
    bundleids = cache.get('bundleids')
    if bundleids is None:
        bundleids = [uuid.uuid4() for _ in range(1000)]
        cache.set('bundleids', bundleids, 24 * 60 * 60)
    entryids = cache.get('entryids')
    if entryids is None:
        entryids = [uuid.uuid4() for _ in range(10000)]
        cache.set('entryids', entryids, 24 * 60 * 60)

    with statsd.pipeline() as pipe, BatchQuery() as b:
        for bundleid in random.sample(bundleids, random.randrange(3)):
            pipe.incr('workloadoutput.bundle.{}.seen'.format(bundleid.hex))
            for entryid in random.sample(entryids, random.randrange(5)):
                pipe.incr('workloadoutput.bundle.{}.{}.seen'.format(
                    bundleid.hex, entryid.hex))
                BundleSeenModel(
                    userid=request.user.id, bundleid=bundleid, entryid=entryid
                ).save()

    return HttpResponse(json.dumps({}), content_type='text/json')
