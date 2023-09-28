from flask import Flask
from ... import db

class Item(db.Model):
    id = db. Column (db. Integer, primary_key=True)

    def __repr_ (self) :
        return f"Item ('{self .id}')"