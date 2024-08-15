import pywikibot
import time
import datetime
from datetime import datetime, timedelta
import re
import getpass
import pywikibot.login as login

password = getpass.getpass("Enter your password: ")
site = pywikibot.Site('simple', 'wikipedia', 'FerienBot2')
site.login(password)

# Protection templates to remove
protection_templates = ["pp", "pp-vandalism", "pp-usertalk", "pp-template", "pp-semi", "pp-salt", "pp-semi-protected", "pp-semi-sock", "pp-semi-spambot", "pp-semi-template", "pp-semi-usertalk", "pp-semi-vandalism", "pp-blp", "pp-dispute"]
protection_templates_str = "|".join(protection_templates)

# Namespaces to check
ADD_NAMESPACES = [0, 1, 4, 5, 9, 11, 12, 13, 14, 15]
REMOVE_NAMESPACES = [0, 1, 2, 3, 4, 5, 9, 11, 12, 13, 14, 15]

def get_protected_pages():
    try:
        logevents = site.logevents(logtype='protect', namespace=ADD_NAMESPACES, total=50)
        protected_pages = set()
        for logevent in logevents:
            page_title = logevent.page().title()
            page = pywikibot.Page(site, page_title)
            if not page.isRedirectPage() and page.exists():
                protected_pages.add(page_title)
    except Exception as e:
        print(f"An error occured: {e}")
    return protected_pages

def get_unprotected_pages():
    recently_unprotected = set()
    try:
        logevents = site.logevents(logtype='protect', namespace=REMOVE_NAMESPACES, user='!=bot', end=datetime.utcnow(), total=50)
        for logevent in logevents:
            if logevent.action == 'unprotect':
                try:
                    title = logevent.title()
                    page = pywikibot.Page(site, title)
                    recently_unprotected.add(title)
                except pywikibot.exceptions.HiddenKeyError:
                    continue
    except pywikibot.exceptions.APIError as e:
        pywikibot.warning(f'API error while fetching unprotected pages: {e}')
    return recently_unprotected


def check_protected_pages(protected_pages):
    for page_title in protected_pages:
        page = pywikibot.Page(site, page_title)
        if not page.protection():
            remove_protection_template(page)
        else:
            add_protection_template(page)

def get_template_pages():
    template_pages = []
    category = pywikibot.Category(site, 'Category:Wikipedia pages with incorrect protection templates')
    for page in category.articles():
        namespace = page.namespace()
        if namespace in REMOVE_NAMESPACES:
            template_pages.append(page)
        else:
            print(f"Skipping page {page.title(as_link=True)} in namespace {namespace}")
    return template_pages

def check_template_pages():
    template_pages = get_template_pages()
    for page in template_pages:
        print("checking cat pages")
        remove_protection_template(page)
    
    recently_unprotected = get_unprotected_pages()
    for page_title in recently_unprotected:
        page = pywikibot.Page(site, page_title)
        remove_protection_template(page)

def add_protection_template(page):
    template = '{{pp|small=yes}}'
    text = page.text
    for protection_template in protection_templates:
        if re.search(r'{{' + re.escape(protection_template) + r'.*?}}\n*', text):
            return
        
    new_text = template + '\n' + text
    summary = 'Bot: Adding protection template'
    try:
        page.text = new_text
        page.save(summary)
    except Exception as e:
        print(f'An error occurred while trying to add the protection template to {page.title()}: {e}')

def remove_protection_template(page):
    text = page.text
    if '{{pp' not in text:
        return
    if page.namespace() not in REMOVE_NAMESPACES:
        return
    new_text = re.sub(r'{{pp.*?}}\n*', '', text)
    summary = 'Bot: Removing protection template'
    try:
        page.text = new_text
        page.save(summary)
    except Exception as e:
        print(f'An error occurred while trying to remove the protection template from {page.title()}: {e}')

while True:
    protected_pages = get_protected_pages()
    check_protected_pages(protected_pages)
    check_template_pages()
    time.sleep(3600)
