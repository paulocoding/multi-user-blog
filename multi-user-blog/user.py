import re
from google.appengine.ext import db
import random
import string
import hashlib

# secret salt for userid has generation
SECRET = "ThisAintVerySecret"

# password hashing functions


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_user_hash(userid, salt):
    return userid + '|' + hashlib.sha256(userid + salt).hexdigest()


def is_userid_valid(h):
    return h == make_user_hash(h.split('|')[0], SECRET)


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)


def valid_login(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)


def getUser(username):
    """Get the user object from the db for provided user name."""
    users = db.GqlQuery("SELECT * FROM User")
    for usr in users:
        if username == usr.name:
            return usr


def userExists(username):
    """Verifiy if the provided username exists in the db."""
    userExists = False
    users = db.GqlQuery("SELECT name FROM User")
    for usr in users:
        if username == usr.name:
            userExists = True
    return userExists


def set_user_cookie(response, user):
    """Set a cookie for provided user."""
    userid = str(user.key().id())
    cookieUser = make_user_hash(userid, SECRET)
    response.set_cookie("user", cookieUser)

# Form fields validation


def valid_username(username):
    """Validating user names."""
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def valid_password(password):
    """Validating passwords."""
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)


def valid_email(email):
    """Validating email addresses."""
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)


class User(db.Model):
    """User class."""

    name = db.StringProperty(required=True)
    pwhash = db.StringProperty(required=True)
    email = db.StringProperty(required=False)

    def set_cookie(self, response):
        """Set a cookie for the current User."""
        userid = str(self.key().id())
        cookieUser = make_user_hash(userid, SECRET)
        response.set_cookie("user", cookieUser)
