from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime

main1 = """<html>
<head>
<title>D'Balls</title>
<h1>D'Balls</h1>
<link rel="stylesheet" href="/Resource/jquery.mobile-1.1.0.min.css" />
<script src="/Resource/jquery-1.7.2.min.js"></script>
<script src="/Resource/jquery.mobile-1.1.0.min.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
</head>
<body align="center">"""

main2 = """</body></html>"""

class Data(db.Model):
    user = db.StringProperty()
    date = db.StringProperty()

class People(db.Model):
    name = db.StringProperty()
    classid = db.StringProperty()

class History(db.Model):
    date = db.StringProperty()
    name = db.StringProperty()
    ball = db.StringProperty()
    status = db.StringProperty()
    
class Entry(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if user.email() == "tan.phengruey.ryan@dhs.sg":
                self.response.out.write(main1 + """<h3>Hi """ + People.get_by_key_name(user.email()).name + """ from """ + People.get_by_key_name(user.email()).classid + """!</h3>""" + """<a href="/balls" data-role="button" data-ajax="false">Balls</a>""")
                self.response.out.write("""<a href="/history" data-role="button" data-ajax="false">History</a>""")
                self.response.out.write("""<a href="%s" data-role="button" data-ajax="false">Log Out</a>""" % users.create_logout_url("/") + main2)
            elif People.get_by_key_name(user.email()):
                self.response.out.write(main1 + """<h3>Hi """ + People.get_by_key_name(user.email()).name + """ from """ + People.get_by_key_name(user.email()).classid + """!</h3>""" + """<a href="/balls" data-role="button" data-ajax="false">Balls</a>""")
                self.response.out.write("""<a href="%s" data-role="button" data-ajax="false">Log Out</a>""" % users.create_logout_url("/") + main2)
            else:
                self.response.out.write(main1 + """<h3>Hi """ + user.nickname() + """!</h3>""" + """<a href="/balls" data-role="button" data-ajax="false">Balls</a>""")
                self.response.out.write("""<a href="%s" data-role="button" data-ajax="false">Log Out</a>""" % users.create_logout_url("/") + main2)
        else:
            self.response.out.write(main1 + """<a href="%s" data-role="button" data-ajax="false">Log In</a>""" % users.create_login_url(self.request.uri) + main2)

class Balls(webapp.RequestHandler):
    def get(self):
        self.response.out.write(main1 + """<a href="/vball" data-role="button" data-ajax="false">Volleyball</a>""")
        self.response.out.write("""<a href="/bball" data-role="button" data-ajax="false">Basketball</a>""")
        self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)

class Volleyball(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if Data.get_by_key_name("vball").user == user.email():
                self.response.out.write(main1 + """Borrowed since: %s""" % Data.get_by_key_name("vball").date)
                self.response.out.write("""<a href="/vball_return" data-role="button" data-ajax="false">Return Volleyball</a>""")
                self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
            elif Data.get_by_key_name("vball").user:
                if People.get_by_key_name(Data.get_by_key_name("vball").user):
                    self.response.out.write(main1 + """Currently Using: %s""" % People.get_by_key_name(Data.get_by_key_name("vball").user).name + """ from %s""" % People.get_by_key_name(Data.get_by_key_name("vball").user).classid)
                    self.response.out.write("""<br>Since: """ + Data.get_by_key_name("vball").date)
                    self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
                else:
                    self.response.out.write(main1 + """Currently Using: %s""" % Data.get_by_key_name("vball").user)
                    self.response.out.write("""<br>Since: """ + Data.get_by_key_name("vball").date)
                    self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
            else:
                self.response.out.write(main1 + """<a href="/vball_loan" data-role="button" data-ajax="false">Loan Volleyball</a>""")
                self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
        else:
            self.response.out.write(main1 + """You do not have permission to do this.""" + main2)

class Volleyball_loan(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if Data.get_by_key_name("vball").user == None:
                Data(key_name = "vball", user = users.get_current_user().email(), date = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%d %B %Y %I:%M %p")).put()
                self.redirect("/vball")
            else:
                self.response.out.write(main1 + """You do not have permission to do this.""" + main2)
        else:
            self.response.out.write(main1 + """You do not have permission to do this.""" + main2)

class Volleyball_return(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if user.email() == Data.get_by_key_name("vball").user:
                Data(key_name = "vball", user = None, date = None).put()
                self.redirect("/vball")
            else:
                self.response.out.write(main1 + """You do not have permission to do this.""" + main2)
        else:
            self.response.out.write(main1 + """You do not have permission to do this.""" + main2)

class Basketball(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if Data.get_by_key_name("bball").user == user.email():
                self.response.out.write(main1 + """Borrowed since: %s""" % Data.get_by_key_name("bball").date)
                self.response.out.write("""<a href="/bball_return" data-role="button" data-ajax="false">Return Basketball</a>""")
                self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
            elif Data.get_by_key_name("bball").user:
                if People.get_by_key_name(Data.get_by_key_name("bball").user):
                    self.response.out.write(main1 + """Currently Using: %s""" % People.get_by_key_name(Data.get_by_key_name("bball").user).name + """ from %s""" % People.get_by_key_name(Data.get_by_key_name("bball").user).classid)
                    self.response.out.write("""<br>Since: """ + Data.get_by_key_name("bball").date)
                    self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
                else:
                    self.response.out.write(main1 + """Currently Using: %s""" % Data.get_by_key_name("bball").user)
                    self.response.out.write("""<br>Since: """ + Data.get_by_key_name("bball").date)
                    self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
            else:
                self.response.out.write(main1 + """<a href="/bball_loan" data-role="button" data-ajax="false">Loan Basketball</a>""")
                self.response.out.write("""<a href="#" data-role="button" data-ajax="false" onClick="parent.history.back()">Back</a>""" + main2)
        else:
            self.response.out.write(main1 + """You do not have permission to do this.""" + main2)

class Basketball_loan(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if Data.get_by_key_name("bball").user == None:
                Data(key_name = "bball", user = users.get_current_user().email(), date = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%d %B %Y %I:%M %p")).put()
                self.redirect("/bball")
            else:
                self.response.out.write(main1 + """You do not have permission to do this.""" + main2)
        else:
            self.response.out.write(main1 + """You do not have permission to do this.""" + main2)

class Basketball_return(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if user.email() == Data.get_by_key_name("bball").user:
                Data(key_name = "bball", user = None, date = None).put()
                self.redirect("/bball")
            else:
                self.response.out.write(main1 + """You do not have permission to do this.""" + main2)
        else:
            self.response.out.write(main1 + """You do not have permission to do this.""" + main2)

class History(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user.email() == "tan.phengruey.ryan@dhs.sg":
            self.response.out.write(main1 + "hi" + main2)
        else:
            self.response.out.write(main1 + """You do not have permission to do this.""" + main2)
        
def main():
    application = webapp.WSGIApplication([('/', Entry),
                                          ('/balls', Balls),
                                          ('/vball', Volleyball),
                                          ('/vball_loan', Volleyball_loan),
                                          ('/vball_return', Volleyball_return),
                                          ('/bball', Basketball),
                                          ('/bball_loan', Basketball_loan),
                                          ('/bball_return', Basketball_return),
                                          ('/history', History)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
