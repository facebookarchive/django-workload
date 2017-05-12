# Async can be introduced gradually. This file contains some async routines
# that are used from a synchronous endpoint.
import asyncio

from .models import FeedEntryModel, UserModel
from .users import suggested_users


def wait_for(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


class Context(object):
    """Shared context among async methods"""
    def __init__(self, request):
        self.endresult = None
        self.prepared = None
        self.request = request
        self.user = self.request.user

    def result_for(self, step):
        return self.prepared.get(step, None)


class AsyncStep(object):
    def __init__(self, context):
        self.context = context

    async def prepare(self):
        """Do work that can be done in parallel"""
        pass

    @property
    def prepared_result(self):
        return self.context.result_for(self)

    def run(self):
        """Execute work in series; all prepare work has completed"""
        pass


class Feed(object):
    def __init__(self, request):
        self.request = request
        self.context = None

    def feed_page(self):
        self.prepare()
        self.run()
        return self.context.endresult

    def prepare(self):
        self.context = context = Context(self.request)
        self.steps = [
            FollowedEntries(context),
            SuggestedUsers(context),
            Assemble(context),
        ]
        self.context.prepared = dict(
            zip(self.steps, wait_for(self.async_prepare())))

    async def async_prepare(self):
        return await asyncio.gather(*(s.prepare() for s in self.steps))

    def run(self):
        for step in self.steps:
            step.run()


class FollowedEntries(AsyncStep):
    async def prepare(self):
        # The Cassandra ORM doesn't offer async support yet, so we'll use a
        # thread executor pool instead
        def fetch_10_posts(user):
            following = user.following
            return list(
                FeedEntryModel.objects.filter(userid__in=following).limit(10))

        def fetch_users(userids):
            return {
                u.id: u for u in UserModel.objects.filter(id__in=list(userids))}

        loop = asyncio.get_event_loop()
        entries = await loop.run_in_executor(
            None, fetch_10_posts, self.context.user)
        userids = {e.userid for e in entries}
        usermap = await loop.run_in_executor(
            None, fetch_users, userids)
        return (entries, usermap)

    def run(self):
        entries, usermap = self.prepared_result
        user = self.context.user
        user_info = {id_: {'name': user.name, 'pk': str(user.id)}
                     for id_, user in usermap.items()}
        self.context.entries = [
            {'entry':{
                'pk': str(e.id),
                'comment_count': e.comment_count,
                'published': e.published.timestamp(),
                'user': user_info[e.userid]
            }}
            for e in entries]

class SuggestedUsers(AsyncStep):
    async def prepare(self):
        def fetch_users(userids):
            return list(UserModel.objects.filter(id__in=userids))

        if len(self.context.user.following) < 25:
            # only suggest when this user isn't following so many people yet
            userids = suggested_users(self.context.user)
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, fetch_users, userids)

    def run(self):
        suggestions = self.prepared_result
        if suggestions:
            self.context.entries.insert(3, {
                'suggestions': [
                    {'name': user.name, 'pk': str(user.id)}
                    for user in suggestions]
            })

class Assemble(AsyncStep):
    def run(self):
        self.context.endresult = {
            'num_results': len(self.context.entries),
            'items': self.context.entries
        }
