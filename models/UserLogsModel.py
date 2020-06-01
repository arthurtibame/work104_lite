from database import db
from models import  CountryModel


class UserLogs(db.Model):
    
    __tablename__ ="userlogs"

    id = db.Column('id', db.Integer, primary_key=True)
    #country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))
    #country_name = db.relationship("Logs", backref=db.backref("country", uselist=False))
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'))
    create_time = db.Column('create_time', db.String(20), index=True)
    modify_time = db.Column('modify_time', db.String(20), index=True)
'''
    def __init__(self, user_id, area_id, create_time, modify_time):
        pass
        #self.user_id = user_id
        #self.area_id = area_id
        #self.create_time = datetime.utcnow()
        #self.modify_time = datetime.utcnow()
    def get_id(self):
        pass
#        return str(self.id)
'''