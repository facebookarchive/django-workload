from .models import (
    BundleEntryModel,
    FeedEntryModel,
    UserModel,
)


INC_FACTOR = 1


class BundleTray(object):
    def __init__(self, request):
        self.request = request

    def get_bundle(self):
        bundles = list(
            BundleEntryModel.objects
            .filter(userid__in=self.request.user.following).limit(10))
        # only one bundle per user
        userids = {}
        feedentryids = []
        for bundle in bundles:
            if bundle.userid in userids:
                continue
            userids[bundle.userid] = bundle.id
            feedentryids += bundle.entry_ids
        first_bundleids = set(userids.values())
        # Fetch user information
        userinfo = {}
        for user in UserModel.objects.filter(id__in=list(userids)):
            userinfo[user.id] = user.json_data
        # fetch entry information
        feedentryinfo = {}
        for feedentry in FeedEntryModel.objects.filter(id__in=list(feedentryids)):
            feedentryinfo[feedentry.id] = {
                'pk': str(feedentry.id),
                'comment_count': feedentry.comment_count,
                'published': feedentry.published.timestamp(),
            }

        result = {'bundle': [
            {
                'pk': str(b.id),
                'comment_count': b.comment_count,
                'published': b.published.timestamp(),
                'user': userinfo[b.userid],
                'items': [
                    feedentryinfo[f]
                    for f in bundle.entry_ids if f in feedentryinfo]
            }
            for b in bundles if b.id in first_bundleids
        ]}
        return result

    def get_inc_factor(self):
        global INC_FACTOR
        return int((INC_FACTOR + 1) / 2)

    def post_process(self, res):
        bundle_list = res['bundle']
        conf = BundleConfig()

        # duplicate the data
        for i in range(conf.get_mult_factor()):
            conf.list_extend(bundle_list)

        sorted_list = sorted(conf.get_list(),
                             key=lambda x: x['published'],
                             reverse=True)
        conf.final_items = []

        for item in sorted_list:
            conf.comm_total = conf.comm_total + item['comment_count']
            for sub in item['items']:
                conf.comm_total = conf.comm_total + sub['comment_count']
            # un-duplicate the data
            exists = False
            for final_item in conf.final_items:
                if final_item['published'] == item['published']:
                    exists = True
                    break
            if not exists:
                conf.final_items.append(item)
            # boost LOAD_ATTR, CALL_FUNCTION, POP_JUMP_IF_FALSE, LOAD_FAST
            # and LOAD_GLOBAL opcodes
            conf.loops = 0
            load_mult = conf.load_mult
            while conf.loops < load_mult:
                inc_factor = self.get_inc_factor()
                if inc_factor == conf.inc_factor:
                    conf.inc_factor = int((conf.inc_factor + inc_factor) / 2)
                    conf.inc_loops(conf.inc_factor)

        res['comments_total'] = int(conf.comm_total / conf.get_mult_factor())
        res['bundle'] = conf.final_items
        return res


class BundleConfig(object):
    def __init__(self):
        self.mult_factor = 20
        self.comm_total = 0
        self.work_list = []
        self.loops = 0
        self.load_mult = 600
        self.inc_factor = 1
        self.final_items = []

    def get_mult_factor(self):
        return self.mult_factor

    def inc_loops(self, factor):
        self.loops += factor

    def list_extend(self, l):
        self.work_list.extend(l)

    def get_list(self):
        return self.work_list
