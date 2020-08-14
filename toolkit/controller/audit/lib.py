import requests
from bs4 import BeautifulSoup, Doctype

def generate_result_bool(audit_json, issues_type, audit_type, score, result = None ):
    audit_json[issues_type]["audits"][audit_type]["score"] = score
    audit_json[issues_type]["audits"][audit_type]["result"] = result
    if result:
        audit_json[issues_type]["audits"][audit_type]["success"] = audit_json[issues_type]["audits"][audit_type]["success"].replace("{value}" , result)

def generate_result_int(audit_json, issues_type, audit_type, score, result = None ):
    audit_json[issues_type]["audits"][audit_type]["score"] = score
    audit_json[issues_type]["audits"][audit_type]["result"] = result
    if result:
        audit_json[issues_type]["audits"][audit_type]["description"] = audit_json[issues_type]["audits"][audit_type]["description"].replace("{value}" , str(result))



def generate_audit_json():
        audit_results = {
            "common_seo_issues":
            {
                "description": "Common Errors",
                "title": "Common SEO Isssues",
                "audits":
                {
                    "meta_title":
                        {
                            "title": "Meta Title Test",
                            "description": "The meta title of your page has a length of {value} characters. Most search engines will truncate meta titles to 70 characters.",
                            "result": None,
                            "score": None,
                            "score_type": "int"
                        },
                    "meta_description":
                        {
                            "title": "Meta Description Test",
                            "description": "The meta description of your page has a length of {value} characters. Most search engines will truncate meta descriptions to 160 characters.",
                            "result": None,
                            "score": None,
                            "score_type": "int"
                        },
                    "robots":
                        {
                            "title": "Robots.txt Test",
                            "success": "Congratulations! Your site uses a 'robots.txt' file: <a href='{value}'>{value}</a>",
                            "error": "Your site doesn't have a 'robots.txt' file",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        },
                    "sitemap":
                        {
                            "title": "Sitemap Test",
                            "success": "Congratulations! Your site has a sitemap: <a href='{value}'>{value}</a>",
                            "error": "Your site doesn't have a sitemap",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        },
                    "https":
                        {
                            "title": "Https Test",
                            "success": "Congratulations! Your website uses https",
                            "error": "Your site doesn't use https. Your ranking will be impacted",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        },
                    "google_analytics":
                        {
                            "title": "Google Analytics Test",
                            "success": "Congratulations! Your webpage is using Google Analytics.",
                            "error": "Google Analytics is recommended for understanding your visitors",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        },
                    "doctype":
                        {
                            "title": "Doctype Test",
                            "success": "Congratulations! Your website has a doctype declaration: {value}",
                            "error": "Your website doesn't have a Doctype declaration",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        }
                }
            }
            

        }
        return audit_results