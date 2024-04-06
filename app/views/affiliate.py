from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from app.tools import helpers, database
from app.tools.utilities import get_file_size, get_root_path, sanitize_filename, get_media_dir, split_filename
from app.models.User import  User
from app.models.Media import  Media
from app.models.Affiliate import  Affiliate
from app.extensions import db
import os

blueprint = Blueprint('affiliate', __name__)

@blueprint.route('/dashboard')
def affiliate_dashboard():
    if "user" in session:
        username = session["user"]
        print("username: ", username)
    
        medias = database.retrieve_from_join(db, User, Media, username)
        file_paths = [database.retrieve(Media, media_id=media.media_id).path for media in medias]
 
        s3_urls = [f"https://<bucket_name>.s3.amazonaws.com/{file_path}" for file_path in file_paths]
   
        return render_template("pages/affiliate/affiliate-dashboard.html")
    
    else:
        return redirect(url_for('login.login'))


@blueprint.route('/about')
def affiliate_about():

    return render_template("pages/affiliate/affiliate-about.html")

@blueprint.route('/affiliate-program/signup')
def affiliate_signup():
    if "user" not in session:
        return redirect(url_for('login.login'))
    
    username = session["user"]
    user = database.retrieve(User, username=username)

    if user.affiliate_id is not None:
        return redirect(url_for('affiliate.affiliate_dashboard'))
    
    
    return render_template("pages/affiliate/affiliate-signup.html")

@blueprint.route('/affiliate-program/register')
def affiliate_register():
    username = session["user"]
    user = database.retrieve(User, username=username)
    print("affiliate_id: ", user.affiliate_id)
    
    key = helpers.generate_key(12)
    database.create(db, Affiliate, key=key)
    user.affiliate_id = database.retrieve(Affiliate, key=key).affiliate_id
    try:
        db.session.commit()
        print("User affiliate_id added!")
    except:
        print("Unable to update user!")

    print("user: ", user.username)
    print("affiliate_id: ", user.affiliate_id)
    print("key: ", key)
    affiliate_key = database.retrieve_from_join(db, User, Media, username)