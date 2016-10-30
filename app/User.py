# -*- coding: utf-8 -*-
import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)

from app.models.user_model import User


class UserSub(UserMixin):
    def __init__(self, email=None, password=None, active=True):
        self.email = email
        self.password = password
        self.active = active
        #self.isAdmin = False
        #self.id = None


    def saveUser(self): 
        print "pre-newUser"
        newUser = User(email=self.email, password=self.password)
        print "pre-save"
        newUser.save()
        print "post-save"
        #print "new user id = %s " % newUser.id
        #self.id = newUser.id
        return self.email

    def get_by_email(self, email):

    	dbUser = User.objects.get(email=email)
    	if dbUser:
            self.email = dbUser.email
            self.active = dbUser.active
            self.id = dbUser.id
            return self
        else:
            return None
    
    def get_by_email_w_password(self, emails):

        try:
            print "hello"
            dbUser = User.objects.get(email=emails)
            
            if dbUser:
                print "dbUser exists"
                self.email = dbUser.email
                #self.active = dbUser.active
                self.password = dbUser.password
                #self.id = dbUser.id
                return self
            else:
                return None
        except:
            print "there was an error"
            return None

    def get_mongo_doc(self):
        if self.id:
            return User.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, id):
    	dbUser = User.objects.with_id(id)
    	if dbUser:
    		self.email = dbUser.email
    		self.active = dbUser.active
    		self.id = dbUser.id

    		return self
    	else:
    		return None



class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"