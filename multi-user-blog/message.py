"""Functions to manage messages between pages using cookies."""


def set_message(response, message):
    """Set a message cookie."""
    response.set_cookie("message", message)


def get_message(request, response):
    """Get and delete the message cookie."""
    message = request.cookies.get('message')
    response.delete_cookie('message')
    return message
