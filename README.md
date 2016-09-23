# Multi User Blog

### A python based blog that supports multiple users, comments and likes.

## Structure
* main.py - Start point
* user.py - User class and related methods
* message.py - Functions to manage messages between pages using cookies
* post.py - Post class and related methods
  * comment.py  - Comment class and related methods
  * like.py -Like class and related methods
* /templates - html templates

## Use
run web app using goggle's appengine.
* Intall appengine
  * https://cloud.google.com/sdk/docs/
* run web server using this command on 'multi-user-blog' project directory
  ```
    $ dev_appserver.py .
  ```
* Open link provided by appengine on a browser

## Link
http://mu-blog.appspot.com/
