"""Auxiliary class and related methods."""
from google.appengine.ext import db


def get_all_likes():
    """Get all likes."""
    likes = db.GqlQuery("SELECT * FROM Post_like")
    return likes


def get_likes_post(post_id):
    """Get the likes for provided post_id."""
    likes = Post_like.all().filter('post_id =', post_id)
    return likes.count()


def liked(user_id, post_id):
    """Check if given user liked given post post_id."""
    liked = Post_like.all().filter('post_id =', post_id)
    liked = liked.filter('user_id =', user_id)
    return liked.count() > 0


class Post_like(db.Model):
    """Post Likes class."""

    user_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)

    def get_id(self):
        """Return current like id."""
        return str(self.key().id())
