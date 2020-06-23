from toolkit.lib.http_tools import request_page

def audit_google_lighthouse_full(url):
    pagespeed = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
    result = request_page(pagespeed + url, timeout=30)
    return result.content

    