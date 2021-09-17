from flask_wtf import FlaskForm 
from wtforms import SubmitField, FileField
from flask_wtf.file import FileRequired, FileAllowed

class UploadForm(FlaskForm):
    file = FileField("Spreadsheet", 
                    validators=[
                        FileRequired(), 
                        FileAllowed(['csv', 'xls', 'xlsx'], "Unsupported format")])
    submit = SubmitField("Submit")
    
