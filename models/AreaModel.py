from database import db




class Area(db.Model):
    __tablename__ = "area"

    id = db.Column('id', db.Integer, primary_key=True)
    #country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    area_id = db.Column('area_id', db.Integer)
    area_en = db.Column('area_en', db.String(10), index=True)
    area_zh_tw = db.Column('area_zh_tw', db.String(10), index=True)
    area_code = db.Column('area_code', db.Integer, unique=True)

        

