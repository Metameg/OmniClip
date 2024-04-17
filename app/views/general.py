from flask import Blueprint, render_template, send_from_directory, session, redirect, url_for
from app.tools import utilities
import os

blueprint = Blueprint('general', __name__)

@blueprint.route('/')
def index():
    return render_template("pages/home.html")

@blueprint.route('/about')
def about():
    return render_template("pages/about.html")

# Invalid URL
@blueprint.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404

# Internal Server Error
@blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template("pages/500.html"), 500

@blueprint.route('/output/<filename>')
def serve_output(filename):
    return send_from_directory(os.path.join(utilities.get_root_path(), 'output'), filename)


@blueprint.route('/<user_dir>/<filename>')
def serve_media(user_dir, filename):
    return send_from_directory(os.path.join(utilities.get_root_path(), user_dir), filename)

@blueprint.route('/loading_container_partial', methods=['GET'])
def loading_container_partial():
    return render_template("partials/loading-container.html")

