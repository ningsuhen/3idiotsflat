'''
Created on Mar 15, 2013

@author: waiky
'''
import webapp2
from google.appengine.api import urlfetch, mail, users
from models.reminders import Reminders
import logging
from settings import JINJA_EMAIL_ENVIRONMENT
import datetime
import re

urlfetch.set_default_fetch_deadline(60)

class ProcessReminders(webapp2.RequestHandler):
    def get(self):
        reminders = Reminders.gql("WHERE lastdismissed < :1", datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).fetch(50)
        logging.info(reminders)
        mail_html = ""
        email_outputs = ""
        if(not reminders == None):
            template = JINJA_EMAIL_ENVIRONMENT.get_template('template.html')
            css_fh = open("email-templates/css/bootstrap-email.min.css", "r")
            bootstrap_for_email_css = css_fh.read()
            css_fh.close()
            reminder_template = JINJA_EMAIL_ENVIRONMENT.get_template('reminder_template.html')
            
            for reminder in reminders:
                reminder_template_values = {
                   'reminder':reminder,
                   'reminder_url':self.request.host_url + "/reminders/" + reminder.key().id_or_name(),
                }
                email_body = reminder_template.render(reminder_template_values)
                
                template_values = {
                   'email_title':'Rent Payment Reminder',
                   'bootstrap_for_email_css': bootstrap_for_email_css,
                   'website_title':'3 Idiots Flat',
                   'home_url':self.request.host_url,
                   'login_url': self.request.host_url + users.create_login_url(self.request.host_url),
                   'email_body':email_body,
                   'email_copy_right': '@copyright: 3 Idiots Flat'
                }
                mail_html = template.render(template_values)
                text_email_body = re.sub(r'<[^>]*?>', '', email_body)
                logging.info(mail_html)
                # #TODO: change email address
                mail.send_mail(sender="3 Idiots Flat <neomysites@gmail.com>",
                # to=",".join(ACTIVE_USER_EMAILS),
                to="ningsuhen@gmail.com",
                subject="Rent Payment Reminder",
                body=text_email_body,
                html=mail_html)
                email_outputs += text_email_body
        self.response.write(email_outputs)

app = webapp2.WSGIApplication([('/tasks/process_reminders', ProcessReminders)])
