from google.appengine.api import users
import webapp2
from controllers.accounts import AccountsPage
from settings import JINJA_ENVIRONMENT, ACTIVE_USER_EMAILS


class MainPage(webapp2.RequestHandler):
    
    
    def get(self):
        user = users.get_current_user()

        if user:
            if(user.email() in ACTIVE_USER_EMAILS or users.is_current_user_admin()):
                template_values = {
                                   'page':{'title':"3 Idiots Flat"},
                                   'user':user,
                                   'active_tab':"home",
                                   'logout_url': users.create_logout_url("/"),
                }
                template = JINJA_ENVIRONMENT.get_template('base.html')
                self.response.write(template.render(template_values))
            else:
                template_values = {
                                   'logout_url': users.create_logout_url("/")
                }
                template = JINJA_ENVIRONMENT.get_template('403.html')
                self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


application = webapp2.WSGIApplication([('/', MainPage), ('/accounts', AccountsPage), ('/tasks/', AccountsPage) ], debug=True)
