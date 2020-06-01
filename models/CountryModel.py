from database import db
from models import  UserLogs


class Country(db.Model):
    
       
    __tablename__ = "country"

    id = db.Column('id', db.Integer, primary_key=True)
    country_name = db.Column('country_name', db.String(20), unique=True,  nullable=False,index=True)
    logs = db.relationship('logs', backref='person', lazy=True)
