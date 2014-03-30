import jinja2

SENDER_EMAIL="3 Idiots Flat <3idiotsflat@example.com>"
ACTIVE_USER_TUPLES = [("user1@example.com", "User1"), ("user2@example.com", "User2")]

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("views"), extensions=['jinja2.ext.autoescape'])
JINJA_EMAIL_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("email-templates"), extensions=['jinja2.ext.autoescape'])


#### to override settings, create a file local_settings.py and override the settings values there
try:
    from local_settings import *
except ImportError:
    pass

ACTIVE_USER_EMAILS = []
ACTIVE_USERS = {}
for active_user in ACTIVE_USER_TUPLES:
    ACTIVE_USER_EMAILS.append(active_user[0])
    ACTIVE_USERS[active_user[0]] = active_user[1]
