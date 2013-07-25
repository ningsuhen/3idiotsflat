import webapp2
from settings import ACTIVE_USER_EMAILS, JINJA_ENVIRONMENT, ACTIVE_USERS
from google.appengine.api import users
from models.reminders import Reminders, ReminderHistory
import logging
import datetime
class ReminderPage(webapp2.RequestHandler):
    def get(self, name=None):
        
        user = users.get_current_user()

        if user and (user.email() in ACTIVE_USER_EMAILS or users.is_current_user_admin()):
            if name is None:
                # generic reminders page - list all reminders
                reminders = Reminders.all().fetch(50)
                template_values = {
                                   'page':{'title':"Reminders"},
                                   'user':user,
                                   'active_tab':"reminders",
                                   'user_emails': ACTIVE_USER_EMAILS,
                                   'users': ACTIVE_USERS,
                                   'reminders':reminders
                }
                template = JINJA_ENVIRONMENT.get_template('reminders/index.html')
                self.response.write(template.render(template_values))
                pass
            else:
                # individual reminder
                
                reminder = Reminders.get_or_insert(key_name=name)
                logging.info(reminder)
                template_values = {
                                   'page':{'title':reminder.description},
                                   'user':user,
                                   'active_tab':"reminders",
                                   'reminder':reminder
                }
                template = JINJA_ENVIRONMENT.get_template('reminders/reminder.html')
                self.response.write(template.render(template_values))
            
        elif (user):
            template_values = {'logout_url': users.create_logout_url("/")}
            template = JINJA_ENVIRONMENT.get_template('403.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def post(self, name=None):
        user = users.get_current_user()

        if user and (user.email() in ACTIVE_USER_EMAILS or users.is_current_user_admin()):
            if name is None:
                # Create New Reminder
                title = self.request.get("title")
                if title == None or title == "":
                    self.response.write("Title cannot be empty or None")
                    return
                # TODO: allow selective reminders
#                 logging.info(self.request.get("targetusers[]"))
                existing_reminder = Reminders.get_by_key_name(title)
                if(existing_reminder == None):
                    reminder = Reminders(key_name=title)
                    reminder.description = self.request.get("description")
                    reminder.put()
                    logging.info(reminder)
                    self.redirect("/reminders/" + title)
                else:
                    self.response.write("Key Already Exists")
            else:
                # name is available, individual reminder
                reminder = Reminders.get_by_key_name(name)
                if(reminder == None):
                    template = JINJA_ENVIRONMENT.get_template('404.html')
                    self.response.write(template.render({}))
                else:
                    # update the reminder
                    if(self.request.get("do") == "Mark Completed"):
                        # complete the reminder
                        reminder.lastdismissed = datetime.datetime.now()
                        reminder.lastupdated = datetime.datetime.now()
                        reminder.snooze = None
                        reminder.save()
                        reminderhistory = ReminderHistory(reminder=reminder)
                        reminderhistory.remarks = self.request.get("remarks")
                        reminderhistory.updatedby = user
                        reminderhistory.update = ReminderHistory.UPDATE_DISMISS
                        reminderhistory.put()
                        self.redirect(self.request.uri)
                    elif(self.request.get("do") == "Snooze"):
                        # update the reminder
                        reminder.lastupdated = datetime.datetime.now()
                        reminder.snooze = int(self.request.get("snooze"))
                        reminder.save()
                        reminderhistory = ReminderHistory(reminder=reminder)
                        reminderhistory.remarks = self.request.get("remarks")
                        reminderhistory.updatedby = user
                        reminderhistory.update = ReminderHistory.UPDATE_SNOOZE
                        reminderhistory.put()
                        self.redirect(self.request.uri)
                    else:
                        template = JINJA_ENVIRONMENT.get_template('error.html')
                        self.response.write(template.render({}))
        elif (user):
            template_values = {'logout_url': users.create_logout_url("/")}
            template = JINJA_ENVIRONMENT.get_template('403.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
        

app = webapp2.WSGIApplication([('/reminders/(.*)', ReminderPage), ('/reminders', ReminderPage)])
