import re
from flask.ext.wtf import Form
from wtforms import HiddenField, validators
from wtforms.validators import DataRequired, Regexp


class AddSnowflake(Form):
    song_id = HiddenField('song_id', validators=[DataRequired(), Regexp("[A-Z0-9]*")])
    img = HiddenField('img', validators=[DataRequired()])
    artist_name = HiddenField('artist_name', validators=[DataRequired()])
    title = HiddenField('title', validators=[DataRequired()])