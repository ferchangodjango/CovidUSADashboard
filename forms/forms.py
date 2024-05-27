from wtforms import StringField,IntegerField,FloatField
from wtforms import validators
from wtforms import Form

class Forms(Form):
    FIRSTNAME=StringField('FIRSTNAME',[validators.DataRequired(),validators.length(max=20)])
    LASTNAME=StringField('LASTNAME',[validators.DataRequired(),validators.length(max=20)])
    FEET=IntegerField('FEET',[validators.DataRequired(),validators.NumberRange(1,10)])
    COMMISION=FloatField('COMMISION',[validators.DataRequired(),validators.NumberRange(0,0.05)])
    IDTIENDA=IntegerField('IDTIENDA',[validators.data_required(),validators.number_range(min=1,max=10)])
    IDF=IntegerField('IDF',[validators.data_required(),validators.number_range(min=1,max=10)])
