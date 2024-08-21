from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.tools import helpers, database, utilities
from app.tools.utilities import get_file_size, get_root_path, sanitize_filename, get_media_dir, split_filename
from app.models.User import  User
from app.models.Render import  Render
from app.extensions import db, csrf
import os, urllib
from datetime import datetime, timedelta, timezone

blueprint = Blueprint('profile', __name__)

@blueprint.route('/retrieve-renders/<string:time_filter>')
def retrieve_renders(time_filter):
    csrf.protect()
    if "user" in session:
        username = session["user"]

        # Get threshold date for time filter selected by user    
        units = time_filter[time_filter.index('=')+1:]
        if 'days' in time_filter:
            threshold_date = datetime.now(timezone.utc) - timedelta(days=int(units)) 
        elif 'hours' in time_filter:
            threshold_date = datetime.now(timezone.utc) - timedelta(hours=int(units)) 

        print("units:", units)
        #FIXME Should be possible to combine these two retrieve queries into one
        try:
            renders = database.retrieve_from_join(db, User, Render, username)
            file_paths = [database.retrieve(Render, Render.timestamp > threshold_date, render_id=render.render_id).path for render in renders]
            # Reverse the order of the files so that the newest render shows first
            file_paths = file_paths[::-1]
        except:
            file_paths = []
            print("No renders found!")

    else:
        return redirect(url_for('login.login'))
    
    html_data = ""
    template = "partials/profile/render-cards.html"

    for path in file_paths:
        path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
        if os.name == 'posix' and not path.startswith('/'):
            path = '/' + path
        directory= os.path.dirname(path)
        filename = os.path.basename(path)
        
        html_data += render_template(template, directory=directory, filename=filename)

    return jsonify(html_data)

@blueprint.route('/remove-profile-render/<path:path>', methods=['GET'])
def remove_render(path):
    csrf.protect()
    file_paths = []
    path = urllib.parse.unquote(path)
    path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
    if os.name == 'posix' and not path.startswith('/'):
        path = '/' + path

    if "user" in session: 
        path = path.replace('/', os.path.sep)

        database.remove(db, Render, path)
        if (os.path.exists(path)):
            os.remove(path)

        s3_urls = [f"https://<bucket_name>.s3.amazonaws.com/{file_path}" for file_path in file_paths]
    else:
        return redirect(url_for('login.login'))

    
    html_data = "data removed"
    # html_data = helpers.build_media_html(file_paths)

    return jsonify(html_data)