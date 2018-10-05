from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms import ValidationError
from wtforms.validators import Required

class SearchForm(Form):
	content = StringField('content',validators=[Required()])
	submit = SubmitField('Submit')
