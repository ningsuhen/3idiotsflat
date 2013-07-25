import jinja2

ACTIVE_USER_EMAILS = ["iamrock10@gmail.com", "ningsuhen@gmail.com", "verizon235@gmail.com"]
ACTIVE_USERS = {ACTIVE_USER_EMAILS[0]: "Kanti", ACTIVE_USER_EMAILS[1]: "Waiky", ACTIVE_USER_EMAILS[2]:"Keshab"}

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("views"), extensions=['jinja2.ext.autoescape'])
JINJA_EMAIL_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("email-templates"), extensions=['jinja2.ext.autoescape'])
