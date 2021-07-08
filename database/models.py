#pylint: disable-all

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref

db = SQLAlchemy()
ma = Marshmallow()



class Img(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, unique = True, nullable = False)
    name = db.Column(db.Text, nullable = False)
    mimetype = db.Column(db.Text, nullable = False)

    def __init__(self, img, name, mimetype):
        self.img = img 
        self.name = name 
        self.mimetype = mimetype

class ImgSchema(ma.Schema):
    class Meta:
        fields = ('img', 'name', 'mimetype')

img_schema = ImgSchema()
img_schemas = ImgSchema(many=True)

def db_init(app):
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()