from flask import current_app as app
from datetime import datetime

@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    if isinstance(value, str):
       return value
    return value.strftime(format)