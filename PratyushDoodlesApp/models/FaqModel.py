from flask import Flask
from .. import db

class Faq(db.Model):
    __tablename__ = 'faq'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Product {self.question} {self.answer}>'