# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from itertools import chain
from operator import itemgetter

from django.core.cache import cache

from .models import (
    FeedEntryModel,
    InboxEntryBase,
    InboxTypes,
    UserModel,
)


class AbstractAggregator(object):
    def add(self, entry):
        pass

    def aggregate(self):
        pass


class Unaggregated(AbstractAggregator):
    def __init__(self):
        self.entries = []

    def add(self, entry):
        self.entries.append(entry.json_data)

    def aggregate(self):
        pass


class LikesAggregator(AbstractAggregator):
    def __init__(self):
        self.per_feedentry = {}

    def add(self, entry):
        self.per_feedentry.setdefault(entry.feedentryid, []).append(entry)

    def aggregate(self):
        feedentries = FeedEntryModel.objects.filter(
            id__in=list(self.per_feedentry))
        feedentry_by_id = {f.id: f for f in feedentries}
        user_by_id = {
            u.id: u for u in UserModel.objects.filter(
                id__in=list({
                    e.likerid
                    for entries in self.per_feedentry.values()
                    for e in entries}))
        }

        def describe(entries):
            users = [user_by_id[e.likerid].name for e in entries]
            if len(users) == 1:
                return '{} liked your post'.format(users[0])
            elif len(users) == 2:
                return '{} and {} liked your post'.format(*users)
            else:
                return '{}, {} and {} others liked your post'.format(
                    users[0], users[1], len(users) - 2)

        self.entries = [
            {
                'type': 'liked',
                'text': describe(entries),
                'published': str(feedentry_by_id[f].published),
            }
            for f, entries in self.per_feedentry.items()]


class FollowersAggregator(AbstractAggregator):
    def __init__(self):
        self.userids = set()
        self.entries = []

    def add(self, entry):
        self.userids.add(entry.followerid)
        self.entries.append(entry)

    def aggregate(self):
        users = UserModel.objects.filter(
            id__in=list(self.userids))
        user_by_id = {u.id: u for u in users}

        self.entries = [
            {
                'type': 'follower',
                'text': '{} started following you'.format(
                    user_by_id[e.followerid].name),
                'userid': e.followerid.hex,
                'published': str(e.published)
            }
            for e in self.entries]


class Inbox(object):
    def __init__(self, request):
        self.request = request

    def load_inbox_entries(self):
        userid = self.request.user.id
        query = InboxEntryBase.objects.filter(userid=userid)
        # clear the _defer_fields entry to ensure we get full results;
        # if we don't only the base model fields are loaded.
        query._defer_fields.clear()
        return query

    def aggregate(self, entries):
        aggregators = {
            InboxTypes.COMMENT: [Unaggregated()],
            InboxTypes.LIKE: [LikesAggregator()],
            InboxTypes.FOLLOWER: [FollowersAggregator()],
        }
        for entry in entries:
            for aggregator in aggregators.get(entry.type, ()):
                aggregator.add(entry)

        for agg in chain.from_iterable(aggregators.values()):
            agg.aggregate()

        entries = chain.from_iterable(
            agg.entries for agg in chain.from_iterable(aggregators.values()))
        return sorted(entries, key=itemgetter('published'), reverse=True)

    def results(self):
        user = self.request.user
        key = 'inbox.{}'.format(user.id.hex)
        cached = cache.get(key)
        if cached is not None:
            return cached

        entries = self.load_inbox_entries()
        result = {'items': self.aggregate(entries)}
        cache.set(key, result, 15)
        return result
