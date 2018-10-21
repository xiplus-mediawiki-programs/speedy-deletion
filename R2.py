# -*- coding: utf-8 -*-
import os
import sys
import pywikibot
import json
from config import *

os.environ['PYWIKIBOT2_DIR'] = os.path.dirname(os.path.realpath(__file__))
os.environ['TZ'] = 'UTC'

if len(sys.argv) < 2:
    exit("no pagename provided.\n")

site = pywikibot.Site()
site.login()

config_page = pywikibot.Page(site, config_page_name)
cfg = config_page.text
cfg = json.loads(cfg)["R2"]
print(json.dumps(cfg, indent=4, ensure_ascii=False))

if not cfg["enable"]:
    exit("disabled\n")

pagename = sys.argv[1]

mainpage = pywikibot.Page(site, pagename)

processPages = []
if mainpage.isRedirectPage():
    if (mainpage.namespace().id in [0, 118]
            and mainpage.getRedirectTarget().namespace().id != mainpage.namespace().id):
        processPages.append(mainpage)
else:
    for backlink in mainpage.backlinks(filter_redirects=True):
        if (backlink.namespace().id in [0, 118]
                and backlink.namespace().id != mainpage.namespace().id):
            processPages.append(backlink)
            continue

print(processPages)
for page in processPages:
    print(page.title())
    
    marked = False
    for template in page.templates():
        if template.title() in ["Template:Delete"]:
            marked = True
            print("marked deletion.\n")
            continue

    if marked:
        continue

    text = cfg["prepend_text"] + page.text
    pywikibot.showDiff(page.text, text)
    page.text = text
    summary = cfg["summary"]
    print(summary)
    input("Save?")
    page.save(summary=summary, minor=False)