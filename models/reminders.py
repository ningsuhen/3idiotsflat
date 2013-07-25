from google.appengine.ext import db
import logging
from google.appengine.api import users

class Reminders(db.Model):
    description = db.StringProperty()
    snooze = db.IntegerProperty()
    lastdismissed = db.DateTimeProperty(auto_now_add=True)
    lastupdated = db.DateTimeProperty(auto_now_add=True)
    # TODO:ALlow selective reminders
    # targetusers = db.ListProperty(users.User)
    
class ReminderHistory(db.Model):
    UPDATE_SNOOZE = "snooze"
    UPDATE_DISMISS = "dismiss"
    reminder = db.Reference(Reminders, collection_name="history")
    historydate = db.DateTimeProperty(auto_now_add=True)
    updatedby = db.UserProperty()
    remarks = db.StringProperty()
    update = db.StringProperty()
