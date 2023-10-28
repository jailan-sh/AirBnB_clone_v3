#!/usr/bin/python3
"""wed api"""

from api.v1.views import app_views


@app_views.route('/status')
def status_f():
    """return status"""
    return jsonify({"status": "OK"})
