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

    def feed_entries(self):
        return FeedEntries.objects(userid=self.id)


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
