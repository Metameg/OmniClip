from flask import Blueprint, render_template, send_from_directory, session, redirect, url_for
import os, urllib

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


@blueprint.route('/renders/<path:user_dir>/<filename>')
def serve_user_render(user_dir, filename):
    env = os.getenv('ENVIRONMENT')
    if env == 'WINDOWS_DEV':
        BASE_DIR = r'D:\\FlaskDemo\\userData\\'
    elif env == 'LINUX_DEV':
        BASE_DIR = '/home/wicker/OmniClip/userData/'
    elif env == 'PRODUCTION':
        BASE_DIR = '/home/wicker/OmniClip/userData/'

    full_dir_path = os.path.join(BASE_DIR, user_dir, 'renders')
    full_dir_path = urllib.parse.unquote(full_dir_path)
    print("full_dir_path; ", full_dir_path)
        
    return send_from_directory(full_dir_path, filename)

@blueprint.route('/<path:user_dir>/<filename>')
def serve_media(user_dir, filename):
    user_dir = urllib.parse.unquote(user_dir)
    
    return send_from_directory(user_dir, filename)

@blueprint.route('/loading_container_partial', methods=['GET'])
def loading_container_partial():
    return render_template("partials/loading-container.html")

# @blueprint.route('/profile_subscription/<selected_pill>/<username>')
# def login_subscription(username, selected_pill):
#     return render_template('pages/profile.html', selected_pill=selected_pill, user=username)
