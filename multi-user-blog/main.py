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
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Post(object):
    """docstring for Post."""
    def __init__(self, title, content, author, likes):
        super(Post, self).__init__()
        self.title = title
        self.content = content
        self.author = author
        self.likes = likes

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

posts = []
posts.append(Post("Post Title", "Lorem ipsum dolor sit amet, consectetur \
                  adipisicing elit, sed do eiusmod tempor incididunt ut labore\
                   et dolore magna aliqua. Ut enim ad minim veniam, quis \
                   nostrud exercitation ullamco laboris nisi ut aliquip ex ea \
                   commodo consequat. Duis aute irure dolor in reprehenderit \
                   in voluptate velit esse cillum dolore eu fugiat nulla \
                   pariatur. Excepteur sint occaecat cupidatat non proident, \
                   sunt in culpa qui officia deserunt mollit anim id est \
                   laborum.", "me", 0))
class MainHandler(Handler):
    def get(self):
        general_error = ""
        self.render("home.html", logged=False, general_error=general_error,
                    posts=posts, user="")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
