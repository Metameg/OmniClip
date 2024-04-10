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

@blueprint.route('/signup')
def affiliate_signup():
    if "user" not in session:
        return redirect(url_for('login.login'))
    
    username = session["user"]
    user = database.retrieve(User, username=username)

    if user.affiliate_id is not None:
        return redirect(url_for('affiliate.affiliate_dashboard'))
    
    
    return render_template("pages/affiliate/affiliate-signup.html")

@blueprint.route('/register', methods=['POST'])
def affiliate_register():
    username = session["user"]
    user = database.retrieve(User, username=username)

    form_copy = dict(request.form)
    for key, value in form_copy.items():
        print(f"{key}: {value}") 
        if value == '':
            form_copy[key] = None

    key = helpers.generate_key(12)
    database.create(db, Affiliate, 
                    first_name=form_copy['first_name'], 
                    last_name=form_copy['last_name'],
                    email=form_copy['email'],
                    addr1=form_copy['addr1'],
                    addr2=form_copy['addr2'],
                    city=form_copy['city'],
                    state=form_copy['state'],
                    zip_code=form_copy['zip_code'],
                    domain=form_copy['domain'],
                    telephone=form_copy['telephone'],
                    business_type=form_copy['business_type'],
                    twitter=form_copy['twitter'],
                    fb=form_copy['fb'],
                    instagram=form_copy['instagram'],
                    youtube=form_copy['youtube'],
                    tiktok=form_copy['tiktok'],
                    twitch=form_copy['twitch'],
                    paypal = form_copy['paypal'],
                    key=key)
    
    user.affiliate_id = database.retrieve(Affiliate, key=key).affiliate_id
    try:
        db.session.commit()
        print("User affiliate_id added!")
    except:
        print("Unable to update user!")

    # retrieve affiliate key given username
    affiliate_key = database.retrieve_from_join(db, User, Media, username)

    return redirect(url_for('login.user'))