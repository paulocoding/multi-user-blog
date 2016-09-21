"""Post class and related methods."""
from google.appengine.ext import db
import like


def get_all_posts():
    """Get all posts."""
    posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
    return posts


def get_post(post_id):
    """Get the post object from the db for id."""
    if post_id.isdigit():
        post_id = int(post_id)
        return Post.get_by_id(post_id)
    else:
        return None


class Post(db.Model):
    """Post class."""

    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author_id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    def get_id(self):
        """Return current post id."""
        return str(self.key().id())

    def like_me(self, user_id):
        """Like the current post."""
        post_id = self.get_id()
        if user_id != self.author_id and not like.liked(user_id, post_id):
            l = like.Post_like(user_id=user_id, post_id=post_id)
            l.put()
            return True
        return False

    def like_count(self):
        """Returns the current post like count."""
        return like.get_likes_post(self.get_id())
