from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from app.models.tutorial import MyUsers

blueprint = Blueprint('user', __name__)

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

@blueprint.route('/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = MyUsers.query.filter_by(email=form.email.data).first()
        if user is None:
            user = MyUsers(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("User Added!")
    our_users = MyUsers.query.order_by(MyUsers.date_added)
    
    return render_template("add_user.html", form=form, name=name, our_users=our_users)