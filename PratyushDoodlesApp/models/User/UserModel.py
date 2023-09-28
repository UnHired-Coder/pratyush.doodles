from flask import Flask
from ... import db

class UserProfile(db.Model):
    id = db.Column(db. Integer, primary_key=True)
    
    def __repr_ (self) :
        return f"UserProfile ('{self .id}')"

class ContactInfo(db.Model):
    id = db.Column(db. Integer, primary_key=True) 

    def __repr_ (self) :
        return f"ContactInfo ('{self .id}')"
