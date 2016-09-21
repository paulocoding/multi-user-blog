#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import user
import post
import message


# setting up jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    """Handler helper methods."""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# posts = []
# posts.append(Post("Post Title", "Lorem ipsum dolor sit amet, consectetur \
#                   adipisicing elit, sed do eiusmod tempor incididunt ut labore\
#                    et dolore magna aliqua. Ut enim ad minim veniam, quis \
#                    nostrud exercitation ullamco laboris nisi ut aliquip ex ea \
#                    commodo consequat. Duis aute irure dolor in reprehenderit \
#                    in voluptate velit esse cillum dolore eu fugiat nulla \
#                    pariatur. Excepteur sint occaecat cupidatat non proident, \
#                    sunt in culpa qui officia deserunt mollit anim id est \
#                    laborum.", "me", 0))
# posts.append(Post("Post 2", "Sed do eiusmod tempor incididunt ut labore\
#                   et dolore magna aliqua. Ut enim ad minim veniam, quis \
#                   nostrud exercitation ullamco laboris nisi ut aliquip ex ea \
#                   commodo consequat. Duis aute irure dolor in reprehenderit \
#                   in voluptate velit esse cillum dolore eu fugiat nulla \
#                   pariatur. Excepteur sint occaecat cupidatat non proident, \
#                   sunt in culpa qui officia deserunt mollit anim id est \
#                   laborum.", "me", 0))


class MainHandler(Handler):
    """Main page."""

    def get(self):
        general_message = message.get_message(self.request, self.response)
        logged_user = user.get_user_logged(self.request)
        posts = post.get_all_posts()
        self.render("home.html", general_message=general_message,
                    posts=posts, user=logged_user)


class SignupHandler(Handler):
    """Signup page."""

    def get(self):
        logged_user = user.get_user_logged(self.request)
        if not logged_user:
            general_message = message.get_message(self.request, self.response)
            error_user = ""
            error_email = ""
            error_pw = ""
            error_verify = ""
            username = ""
            email = ""
            self.render("signup.html", general_message=general_message,
                        username=username, email=email,
                        error_user=error_user, error_email=error_email,
                        error_pw=error_pw, error_verify=error_verify)
        else:
            self.redirect('/')

    def post(self):
        # getting form values
        username = self.request.get("username")
        pw = self.request.get("password")
        pw2 = self.request.get("verify")
        email = self.request.get("email")

        # initializing error messages
        general_message = message.get_message(self.request, self.response)
        error_user = ""
        error_email = ""
        error_pw = ""
        error_verify = ""

        # validating form

        userValid = user.valid_username(username)
        userExists = False
        if userValid:
            userExists = user.userExists(username)
        pwValid = user.valid_password(pw)
        pwMatch = pw == pw2
        emailValid = True
        if email:
            emailValid = user.valid_email(email)
        else:
            email = ''

        if not userValid:
            error_user = 'Invalid Name'
        if userExists:
            error_user = 'User name already taken'
        if not pwValid:
            error_pw = 'Invalid password'
        if not pwMatch:
            error_verify = "Passwords don't match"
        if not emailValid:
            error_email = 'Invalid email'

        if userValid and pwValid and pwMatch and emailValid and not userExists:
            # generate password Hash
            pwhash = user.make_pw_hash(username, pw)
            # save user to db
            u = user.User(name=username, pwhash=pwhash, email=email)
            u.put()
            # set user cookie
            u.set_cookie(self.response)

            self.redirect('welcome')
        else:
            self.render("signup.html", logged=False,
                        general_message=general_message,
                        username=username, email=email,
                        error_user=error_user, error_email=error_email,
                        error_pw=error_pw, error_verify=error_verify)


class LogoutHandler(Handler):
    """logout current user."""

    def get(self):
        user.del_user_cookie(self.response)
        message.set_message(self.response, "You have logged out.")
        self.redirect('/signup')


class LoginHandler(Handler):
    """logout current user."""

    def get(self):
        logged_user = user.get_user_logged(self.request)
        if not logged_user:
            general_message = message.get_message(self.request, self.response)
            error_login = ""
            self.render("login.html", general_message=general_message,
                        error_login=error_login)
        else:
            self.redirect('/')

    def post(self):
        logged_user = user.get_user_logged(self.request)
        if not logged_user:
            username = self.request.get("username")
            pw = self.request.get("password")
            pwValid = user.valid_password(pw)
            userValid = user.valid_username(username)
            if pwValid and userValid:
                user_obj = user.get_user(username)
                if user.valid_login(username, pw, user_obj.pwhash):
                    # set cookie
                    user_obj.set_cookie(self.response)
                    self.redirect('/welcome')
            general_message = message.get_message(self.request, self.response)
            error_login = "Invalid Login"
            self.render("login.html", general_message=general_message,
                        error_login=error_login)
            message.set_message(self.response, "You are now logged in")
        else:
            self.redirect('/')


class WelcomeHandler(Handler):
    """Welcomes user to the site."""

    def get(self):
        logged_user = user.get_user_logged(self.request)
        if logged_user:
            general_message = message.get_message(self.request, self.response)
            self.render("welcome.html", general_message=general_message,
                        user=logged_user)
        else:
            self.redirect('/')


class NewPostHandler(Handler):
    """New Post form."""

    def get(self):
        logged_user = user.get_user_logged(self.request)
        if logged_user:
            general_message = message.get_message(self.request, self.response)
            error_post = ""
            self.render("new_post.html", general_message=general_message,
                        user=logged_user, error_post=error_post)
        else:
            self.redirect('/login')

    def post(self):
        logged_user = user.get_user_logged(self.request)
        if logged_user:
            title = self.request.get('title')
            content = self.request.get('content')
            if title and content:
                new_post = post.Post(title=title, content=content,
                                     author_id=logged_user.get_id())
                new_post.put()
                message.set_message(self.response, "'%s' post added." % title)
                self.redirect('/')
            else:
                general_message = ""
                error_post = "Please fill in both title and post:   "
                self.render("new_post.html", general_message=general_message,
                            user=logged_user, error_post=error_post,
                            title=title, content=content)

        else:
            self.redirect('/login')


class PostHandler(Handler):
    """Individual post page."""

    def get(self, post_id):
        logged_user = user.get_user_logged(self.request)
        general_message = message.get_message(self.request, self.response)
        current_post = post.get_post(post_id)
        if current_post:
            self.render("post.html", general_message=general_message,
                        user=logged_user, post=current_post)
        else:
            self.render("no_post.html", general_message=general_message,
                        user=logged_user)


class DeletePostHandler(Handler):
    """Delete post page."""

    def get(self, post_id):
        logged_user = user.get_user_logged(self.request)
        current_post = post.get_post(post_id)
        if current_post:
            if logged_user.get_id() == current_post.author_id:
                message.set_message(self.response,
                                    "'%s' post deleted." % current_post.title)
                current_post.delete()
                self.redirect('/')
            else:
                message.set_message(self.response,
                                    "Only the post author can delete a post")
                self.redirect('/')

        else:
            general_message = message.get_message(self.request, self.response)
            self.render("no_post.html", general_message=general_message,
                        user=logged_user)


class LikePostHandler(Handler):
    """Individual post page."""

    def get(self, post_id):
        logged_user = user.get_user_logged(self.request)
        current_post = post.get_post(post_id)
        if current_post:
                if current_post.like_me(logged_user.get_id()):
                    message.set_message(self.response, "Post Liked")
                else:
                    message.set_message(self.response, "Post already Liked")
                self.redirect('/')

        else:
            general_message = message.get_message(self.request, self.response)
            self.render("no_post.html", general_message=general_message,
                        user=logged_user)


class EditPostHandler(Handler):
    """Individual post page."""

    def get(self, post_id):
        logged_user = user.get_user_logged(self.request)
        current_post = post.get_post(post_id)
        general_message = message.get_message(self.request, self.response)
        if current_post and current_post.author_id == logged_user.get_id():
            self.render("edit_post.html", general_message=general_message,
                        user=logged_user, title=current_post.title,
                        content=current_post.content)
        else:
            self.render("no_post.html", general_message=general_message,
                        user=logged_user)

    def post(self, post_id):
        logged_user = user.get_user_logged(self.request)
        current_post = post.get_post(post_id)
        if logged_user and current_post.author_id == logged_user.get_id():
            title = self.request.get('title')
            content = self.request.get('content')
            if title and content:
                current_post.title = title
                current_post.content = content
                current_post.put()
                message.set_message(self.response, "'%s' post edited." % title)
                self.redirect('/')
            else:
                general_message = ""
                error_post = "Please fill in both title and post:   "
                self.render("edit_post.html", general_message=general_message,
                            user=logged_user, title=title,
                            error_post=error_post, content=content)

        else:
            message.set_message('Only the author can edit this post.')
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/logout', LogoutHandler),
    ('/signup', SignupHandler),
    ('/login', LoginHandler),
    ('/welcome', WelcomeHandler),
    ('/new', NewPostHandler),
    ('/post/(\d+)', PostHandler),
    ('/like/(\d+)', LikePostHandler),
    ('/edit/(\d+)', EditPostHandler),
    ('/delete/(\d+)', DeletePostHandler)
], debug=True)
