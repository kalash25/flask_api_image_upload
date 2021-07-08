#pylint: disable-all

from flask import Flask, json, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from uploading_images.database.models  import Img, db_init, db
from database.models import Img, db_init, db
from werkzeug.utils import secure_filename #this is to read our file name securely
import os 


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db_init(app)

@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic:
        return jsonify({"code": 404})

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype 

    img = Img(img=pic.read(), mimetype=mimetype, name= filename)
    db.session.add(img)
    db.session.commit()

    return jsonify({"code": 200})

    
@app.route('/<int:id>')
def get_img(id):
    img = Img.query.get(id)
    # img = Img.query.filter_by(id=id).first()

    if not img:
        return jsonify({"code": 404})

    return Response(img.img, mimetype=img.mimetype)


# IF WE WANT TO SEARCH FOR FILE BASED ON NAME
# NEED TO CHANGE THE FILENAME ON TOP TO THE DESIRED ONE DURING UPLOAD FOR THIS TO WORK

# @app.route('/<filename>')
# def get_img(filename):
#     # img = Img.query.get(filename)
#     img = Img.query.filter_by(name=filename).first()

#     if not img:
#         return jsonify({"code": 404})

#     return Response(img.img, mimetype=img.mimetype)


app.run(debug=True)

