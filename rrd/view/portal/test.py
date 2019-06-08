


import re


def remove_html(raw_html):
    cleanr = re.compile("<A.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</A>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<div.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</div>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<img.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</img>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<i.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</i>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    raw_html = raw_html.replace("&nbsp;",'')
    return raw_html

print(remove_html(aa))