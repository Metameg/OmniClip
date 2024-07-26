from flask import Blueprint, request, jsonify, session
from app.tools import helpers, database, utilities
from app.tools.utilities import get_file_size, get_root_path, sanitize_filename, get_media_dir, split_filename
from app.models.User import  User
from app.models.Media import  Media
from app.extensions import db
import os, urllib

blueprint = Blueprint('profile', __name__)

@blueprint.route('/retrieve-renders', methods=['POST'])
def upload_renders():
    pass

def retrieve_renders():
    pass