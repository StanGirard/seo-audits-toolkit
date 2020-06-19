from toolkit.lib.http_tools import request_parse, request_status_code

def find_all_headings(soup):
    headings = {"h1": {"count": 0, "values": []}, "h2": {"count": 0, "values": []},
                "h3": {"count": 0, "values": []}, "h4": {"count": 0, "values": []},
                "h5": {"count": 0, "values": []}, "h6": {"count": 0, "values": []}}
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        headings[heading.name]["values"].append(heading.text.strip())
        headings[heading.name]["count"] += 1
    return headings

def find_all_headers_url(url):
    soup = request_parse(url)
    if soup:
        return find_all_headings(soup)
    else:
        return {"Error": "No headers found or error in the url"}



def print_all_headers(headers_list):
    for key in headers_list:
        for i in headers_list[key]["header"]:
            print(key + " " + i)


def print_specific_header(headers_list, header):
    for i in headers_list[header]["header"]:
        print(header + " " + i)


def print_all_headers_count(headers_list):
    for key in headers_list:
        print("Number of " + key + " : " + str(headers_list[key]["count"]))


def print_specific_header_count(headers_list, header):
    print("Number of " + header + " : " + str(headers_list[header]["count"]))
