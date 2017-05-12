# models represent mock data, here to drive Python and Cassandra to produce
# reasonably realistic I/O.
import datetime
import uuid

from cassandra.cqlengine import columns
from cassandra.util import uuid_from_time, datetime_from_uuid1
from django_cassandra_engine.models import DjangoCassandraModel


def timeuuid_now():
    return uuid_from_time(datetime.datetime.now())


class UserModel(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()
    following = columns.List(columns.UUID)

    def feed_entries(self):
        return FeedEntryModel.objects(userid=self.id)

    # allow this to be used as request.user without breaking expectations
    def is_authenticated(self):
        return True


class FeedEntryModel(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'id'

    userid = columns.UUID(primary_key=True)
    id = columns.TimeUUID(
        primary_key=True, default=timeuuid_now, clustering_order="DESC")
    comment_count = columns.SmallInt(default=0)

    @property
    def published(self):
        return datetime_from_uuid1(self.id)


class BundleSeenModel(DjangoCassandraModel):
    class Meta:
        # required but meaningless in this context
        get_pk_field = 'userid'

    userid = columns.UUID(primary_key=True)
    bundleid = columns.UUID(primary_key=True)
    ts = columns.TimeUUID(
        primary_key=True, default=timeuuid_now, clustering_order="DESC")
    entryid = columns.UUID()
