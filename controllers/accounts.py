from google.appengine.api import users
import webapp2
from models.accounts import Accounts, Contribution
import datetime

from settings import JINJA_ENVIRONMENT, ACTIVE_USERS, ACTIVE_USER_EMAILS
from google.appengine.api.users import User
from google.appengine.ext.db import GqlQuery
import logging

def get_sorted_keys(d, reverse=False):
    return sorted(d, key=d.get, reverse=reverse)

class AccountsPage(webapp2.RequestHandler):
    
    def get(self):
        self.accounts_page()
        
    def post(self):
        self.accounts_page()
    
        
        
    def accounts_page(self):
        user = users.get_current_user()

        if user and (user.email() in ACTIVE_USER_EMAILS or users.is_current_user_admin()):
            reloadPage = False
            simpleText = False
            usedby = {}
            user_amount_map = {}
            user_adjustment = {}
            paymentMap = {}
            error_message = ""
            calculation_error = ""
            total_amount = 0
            
            if(self.request.get('simpletext') and self.request.get('simpletext') == "True"):
                simpleText = True
                
                
            # split month into tokens
            month = self.request.get('month') if (self.request.get('month') and not self.request.get('month') == "")  else datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
            # if there's a cmd param
            if(self.request.get('cmd')):
                if(self.request.get('cmd') == "delete"):
                    eid = long(self.request.get('eid'))
                    entry = Accounts.get_by_id(eid)
                    entry.deleted = True
                    entry.put()
                    self.redirect('/accounts')
                    return
                else:
                    description = self.request.get('description') if  (self.request.get('description') and not self.request.get('description') == "") else False
                
                    error_messages = []
                    if(not description):
                        error_messages.append("Description is mandatory")
                    
                    amount = self.request.get('amount') if (self.request.get('amount') and not self.request.get('amount') == "") else False
                    if(not amount):
                        error_messages.append("Amount is mandatory")
                    try:
                        int(amount)
                    except:
                        error_messages.append("Amount should be a number")
                    
                    expenseby = self.request.get('expenseby') if (self.request.get('expenseby') and not self.request.get('expenseby') == "") else False
                    if(not expenseby):
                        error_messages.append("Expense by is mandatory")
    
                    # TODO: fix this
                    expenseby = User(expenseby)
                    
                    count = 0
                    user_objects = {}
    
                    for email in ACTIVE_USER_EMAILS:
                        current_user = User(email)
                        user_objects[email] = current_user
                        usedby[email] = 1 if (self.request.get(email) and self.request.get(email) == "on") else 0
                        if(usedby[email] == 1):
                            count += 1
                        
                        
                    
    #                 all = 1 if (self.request.get('all') and self.request.get('all') == "on") else 0
                    if(count == 0):
                        error_messages.append("Atleast one person should be selected")
                    
                    if(len(error_messages) == 0):
                        amount = int(amount)
                        individual_amount = amount / count
                        # #Add new entry 
                        newAccountEntry = Accounts()
                        newAccountEntry.expenseby = expenseby
                        newAccountEntry.expensefor = description
                        newAccountEntry.expenseamount = amount
                        newAccountEntry.expensemonth = datetime.date.today().replace(day=1)
                        newAccountEntry.put()
                        
                        for email, current_user in user_objects.iteritems():
                            contribution = Contribution(account=newAccountEntry)
                            contribution.contributor = current_user
                            if(current_user == expenseby):
                                if(usedby[email] == 1):
                                    contribution.amount = float(individual_amount - amount)
                                else:
                                    contribution.amount = float(0 - amount)
                            else:
                                if(usedby[email] == 1):
                                    contribution.amount = float(individual_amount)
                                else:
                                    contribution.amount = float(0)
                            contribution.put()
                        """ 
                         description=""
                        amount=""
                        expenseby=""
                        usedby = [] """
                        reloadPage = True
                    else:
    
                        for error in error_messages:
                            error_message += "[x] " + error + "<br />"
                    
                    # GqlQuery("SELECT DISTINCT expensedate ")
                
                
            q = GqlQuery("SELECT DISTINCT expensemonth FROM Accounts")
            available_months = q.fetch(24)  # let's limit to 2 yrs
            expenses = Accounts.gql("WHERE expensemonth=DATE('" + month + "') ORDER BY expensedate DESC").fetch(1000)
            for expense in expenses:
                if not expense.deleted:
                    total_amount += expense.expenseamount
                for contribution in expense.contributions:
                    if not expense.deleted:
                        if(not contribution.contributor.email() in user_amount_map):
                            user_amount_map[contribution.contributor.email()] = 0
                        user_amount_map[contribution.contributor.email()] += contribution.amount
                    setattr(expense, contribution.contributor.email(), contribution.amount)
            if (total_amount > 0):
                user_adjustment = user_amount_map.copy()
                asc_adjustment_keys = get_sorted_keys(user_adjustment)
                logging.info("asc_adjustment_keys: %s" % (asc_adjustment_keys))
                desc_amount_keys = get_sorted_keys(user_amount_map, True)
                minUser = asc_adjustment_keys[0]
                
                for mapuser in desc_amount_keys:
                    logging.info("user_adjust_ment: %s" % (user_adjustment))
                    if(user_adjustment[minUser] < 0 and not user_adjustment[mapuser] == 0 and mapuser != minUser):
                        # calcualte amount to pay
                        payamount = user_adjustment[mapuser]
                        user_adjustment[minUser] += payamount
                        user_adjustment[mapuser] = 0
                        logging.info("user_adjust_ment: %s" % (user_adjustment))
                        paymentMap[mapuser] = [minUser, payamount]
                    elif int(user_adjustment[mapuser]) > 0:
                        logging.error("calculation error: " + str(user_adjustment[mapuser]) + " " + mapuser + "" + minUser)
                        calculation_error = "calculation error: " + str(user_adjustment[mapuser]) + " " + mapuser + "" + minUser
                        
                    asc_adjustment_keys = get_sorted_keys(user_adjustment)
                    minUser = asc_adjustment_keys[0]
            template_values = {
                               'page':{'title':"Accounts"},
                               'user':user,
                               'error_message': error_message,
                'simpleText': simpleText,
                'logout_url': users.create_logout_url("/"),
                'active_tab': "accounts",
                'reloadPage': reloadPage,
                'user_emails': ACTIVE_USER_EMAILS,
                'users': ACTIVE_USERS,
                'available_months': available_months,
                'usedby': usedby,
                'paymentMap': paymentMap,
                'expenses': expenses,
                'calculation_error':calculation_error,
                'totals': {'amount':total_amount, 'useramounts': user_amount_map}
            }
            template = JINJA_ENVIRONMENT.get_template('accounts/index.html')
            self.response.write(template.render(template_values))
        elif (user):
            template_values = {'logout_url': users.create_logout_url("/")}
            template = JINJA_ENVIRONMENT.get_template('403.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
