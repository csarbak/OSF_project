"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass

class SignupForm(FlaskForm):
    """User Sign-up Form."""

    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ],
    )
    confirm = PasswordField(
        "Confirm Your Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    website = StringField("Website", validators=[Optional()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """User Log-in Form."""

    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class SymbolForm(FlaskForm):
    """ Symbol Form."""

    exchange_name = SelectField(
        "Exchange name",
        [DataRequired()],
        choices=[
            ("BX", "BX"),
            ("nasdaq", "nasdaq"),
            ("PHLX", "PHLX")
        ]
    )
    symbol =  NonValidatingSelectField(
        "Symbol",
        choices=[]
    )

    submit = SubmitField("submit")



class MyForm(FlaskForm):
    country = SelectField('Country', choices=[('usa', 'USA'), ('can', 'Canada')])
    city = SelectField('City', choices=[])
    
