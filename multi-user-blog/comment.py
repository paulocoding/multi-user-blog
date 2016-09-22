"""Post class and related methods."""
from google.appengine.ext import db


def get_comments(post_id):
    """Get all the comments for a given post."""
    comments = Comment.all().filter('post_id =', post_id).order('-created')
    return comments


def del_comments(post_id):
    """Delete all the comments for a given post."""
    comments = Comment.all().filter('post_id =', post_id)
    for c in comments:
        c.delete()


class Comment(db.Model):
    """Comment class."""

    content = db.TextProperty(required=True)
    author_name = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    def get_id(self):
        """Return current comment id."""
        return str(self.key().id())
