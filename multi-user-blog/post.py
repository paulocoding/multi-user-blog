"""Post class and related methods."""
from google.appengine.ext import db


def get_all_posts():
    """Get all posts."""
    posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
    return posts


def get_post(post_id):
    """Get the post object from the db for id."""
    return Post.get_by_id(post_id)


class Post(db.Model):
    """Post class."""

    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author_id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    def get_id(self):
        return self.key().id()
