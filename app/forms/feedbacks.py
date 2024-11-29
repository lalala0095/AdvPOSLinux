from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, DecimalField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, InputRequired

class FeedbackForm(FlaskForm):
    client_name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[Optional()])
    contact_number = IntegerField("Contact Number", validators=[Optional()])
    feedback_type = SelectField("Type", choices=[
        ("Feedback", "Feedback"),
        ("Issue", "Issue"),
        ("Others", "Others")
    ], validators=[DataRequired()])
    feedback_urgency = SelectField("Urgency", choices=[
        ("Urgent", "Urgent"),
        ("Normal", "Normal"),
        ("Low", "Low")
    ], validators=[DataRequired()])
    details = TextAreaField("Details", validators=[DataRequired()])
    submit = SubmitField("Submit")
