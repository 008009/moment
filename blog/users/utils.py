import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from blog import app

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	pic_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)
	output_size = (125, 125 )
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return pic_fn