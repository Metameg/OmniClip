from flask import Blueprint, request, jsonify, session, render_template
from app.tools import helpers, database, utilities
from app.tools.utilities import get_file_size, get_root_path, sanitize_filename, get_media_dir, split_filename
from app.models.User import  User
from app.models.Render import  Render
from app.extensions import db
import os, urllib

blueprint = Blueprint('profile', __name__)

@blueprint.route('/retrieve-renders')
def retrieve_renders():
    username = session["user"]
    renders = database.retrieve_from_join(db, User, Render, username)
    file_paths = [database.retrieve(Render, render_id=render.render_id).path for render in renders]
    s3_urls = [f"https://<bucket_name>.s3.amazonaws.com/{file_path}" for file_path in file_paths]
    html_data = ""
    template = "partials/uploader/all-media.html"

    for path in file_paths:
        directory= os.path.dirname(path)
        filename = os.path.basename(path)
        html_data += render_template(template, directory=directory, filename=filename)

    return jsonify(html_data)

