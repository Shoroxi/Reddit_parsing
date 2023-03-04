import praw
import logging

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# for logger_name in ("praw", "prawcore"):
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(handler)


class Reddit:
    def __init__(self, **kwargs):
        self.reddit = praw.Reddit(**kwargs, check_for_async=False)

    def get_posts_from(self, name, **mode):
        if mode['sort'] in ['hot', 'new', 'rising']:
            posts = eval(f"self.reddit.subreddit(name).{mode['sort']}(limit={mode['limit']})")
        else:
            return

        data = [{
                    # 'title': post.title,
                    'url': post.url,
                    'created_at': post.created,
                    'spoiler': post.spoiler,
                    'stickied': post.stickied,
                    'pinned': post.pinned,
                    'link_flair_text': post.link_flair_text,
                    'permalink': post.permalink,
                    'sub_name': post.subreddit_name_prefixed,
                    'ups': post.ups,
                    # 'is_video': post.is_video,
                    # 'is_reddit_media_domain': post.is_reddit_media_domain,
                    # 'is_gallery': post.is_gallery,
                    'domain': post.domain, # 'i.imgur.com' # giphy.com #
                    # 'media_only': post.media_only
                    # 'media': post.media['reddit_video']['fallback_url'],
                    # 'gif': post.media['reddit_video']['is_gif']
                    # 'post_hint': 'image',
                    # 'over_18': True,
                    }
                for post in posts]

        return data

    def get_new_posts_from_array(self, name, **mode):
        new_data = self.get_posts_from(name, **mode)
        
        new_posts = []
        for post in new_data:
            new_posts.append(post)
        
        return new_posts
    
    def get_latest_posts(self, name, data, attach=False, **mode):
        new_data = self.get_posts_from(name, **mode)

        dpost = 1 if attach else 0

        if data[dpost] in new_data:
            index = new_data.index(data[dpost])
            if index != dpost:
                return [post for post in new_data[:index]]
