from google.appengine.ext import db
import logging

class Accounts(db.Model):
    expensedate = db.DateTimeProperty(auto_now_add=True)
    expenseby = db.UserProperty()
    expensefor = db.StringProperty()
    expensemonth = db.DateProperty()
    expenseamount = db.IntegerProperty()
    deleted = db.BooleanProperty()
    
    def __init__(self, parent=None,
               key_name=None,
               _app=None,
               _from_entity=False,
               **kwds):
        super(Accounts, self).__init__(parent, key_name, _app, _from_entity, **kwds)
        if(self.deleted == None):
            self.deleted = False
        self.contribution_map = None
            
    def get_contribution_by_email(self, email):
        if(self.contribution_map == None):
            self.contribution_map = {}
            for contribution in self.contributions:
                if(contribution.contributor != None):
                    self.contribution_map[contribution.contributor.email()] = contribution.amount
                logging.info(contribution.contributor)
        if(not email in self.contribution_map):
            return 0
        else:
            return self.contribution_map[email]

class Contribution(db.Model):
    account = db.ReferenceProperty(Accounts, collection_name="contributions")
    contributor = db.UserProperty()
    amount = db.FloatProperty()
    deleted = db.BooleanProperty()
    
    def __init__(self, parent=None,
               key_name=None,
               _app=None,
               _from_entity=False,
               **kwds):
        super(Contribution, self).__init__(parent, key_name, _app, _from_entity, **kwds)
        if(self.deleted == None):
            self.deleted = False

# class Contributers():
