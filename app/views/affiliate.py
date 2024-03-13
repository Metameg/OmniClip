from flask import Blueprint, render_template

blueprint = Blueprint('affiliate', __name__)

@blueprint.route('/dashboard')
def affiliate_dashboard():
    return render_template("pages/affiliate/affiliate-dashboard.html")



@blueprint.route('/about')
def affiliate_about():
    return render_template("pages/affiliate/affiliate-about.html")