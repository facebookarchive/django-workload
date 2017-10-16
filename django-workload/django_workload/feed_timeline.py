class FeedTimeline(object):
    def __init__(self, request):
        self.request = request

    def get_timeline(self):
            user = self.request.user
            feed = user.feed_entries().limit(20)
            user_info = user.json_data
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
            return result

    def get_inc_factor(self):
        result = int((1 + 1) / 2)
        return result

    def post_process(self, result):
        item_list = result['items']
        conf = FeedTimelineConfig()

        # duplicate the data
        for i in range(conf.mult_factor):
            conf.list_extend(item_list)

        sorted_list = sorted(conf.get_list(),
                             key=lambda x: x['published'],
                             reverse=True)
        final_items = []

        for item in sorted_list:
            conf.user = item['user']['name']
            conf.comments_total = conf.comments_total + item['comment_count']
            conf.comments_per_user[conf.user] = item['comment_count']
            # un-duplicate the data
            exists = False
            for final_item in final_items:
                if final_item['pk'] == item['pk']:
                    exists = True
                    break
            if not exists:
                final_items.append(item)
            # boost LOAD_ATTR and CALL_FUNCTION opcodes
            conf.loops = 0
            load_mult = conf.load_mult
            while conf.loops < load_mult:
                conf.inc_loops(self.get_inc_factor())

        result['comments_total'] = int(conf.comments_total / conf.mult_factor)
        result['items'] = final_items
        return result


class FeedTimelineConfig(object):
    def __init__(self):
        # Number of times the original items list is duplicated in order
        # to make the view more Python intensive
        self.mult_factor = 5
        self.work_list = []
        self.user = ""
        self.comments_total = 0
        self.comments_per_user = {}
        self.loops = 0
        # Number of times the while loop in post_process is executed, in order
        # to obtain a representative opcode usage for real-life scenarios
        self.load_mult = 1000

    def inc_loops(self, factor):
        self.loops += factor

    def list_extend(self, l):
        self.work_list.extend(l)

    def get_list(self):
        return self.work_list
