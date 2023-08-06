__version__ = "0.2.0a1"

import os
import json
import atila
import skitai
from skitai.wastuff.api import ISODateTimeWithOffsetEncoder
import re

RX_SPACE = re.compile (r'\s+')
ROUTES_CACHE = {}
VIEWS_DIR = "/apps"

def __config__ (pref):
    pref.config.MINIFY_HTML = 'strip'


def __setup__ (app, mntopt):
    from skitai.wastuff import sendmail

    if "SMTP" in app.config:
        smtp = app.config.SMTP
        sendmail.configure (smtp ["SMTP_SERVER"], smtp ["SMTP_AUTH"], smtp ["SMTP_SENDER"])

    @app.route ('/status')
    @app.permission_required (skitai.isdevel () and ['user'] or ['staff'])
    def status (was, f = ''):
        return was.status (f)

    # template globals ------------------------------------
    @app.template_global ('raise')
    def raise_helper (was, msg):
        raise Exception (msg)

    @app.template_global ('build_routes')
    def build_routes (was, base):
        def collect (start, base_len):
            pathes = []
            for fn in os.listdir (start):
                path = os.path.join (start, fn)
                if path.endswith ('/components'):
                    continue
                if os.path.isdir (path):
                    pathes.extend (collect (path, base_len))
                elif fn.endswith ('.vue'):
                    pathes.append ((
                        path [base_len:-4].replace ("\\", '/').replace ('/_', '/:'),
                        path [base_len:].replace ("\\", '/'),
                    ))
            return pathes

        def find (root):
            if not os.path.isdir (root):
                return None, []

            routes = []
            pathes = []
            names = set ()
            for path, vue in collect (root, len (root)):
                if path.endswith ('/index'):
                    path = path [:-6] or '/'
                vue_path = "{}{}{}".format (VIEWS_DIR, base, vue)
                if path == '/':
                    routes.append ('{name: "%s", path: "%s", component: () => loadModule("%s", options)}' % (path [1:] or 'index', path, vue_path))
                    was.push (vue_path) # server push
                else:
                    if vue_path.endswith ('/index.vue'):
                        routes.append ('{name: "%s", path: "%s", component: () => loadModule("%s", options)}' % (path [1:] or 'index', path, vue_path))
                    else:
                        routes.append ('{name: "%s", path: "%s", component: Vue.defineAsyncComponent ( () => loadModule("%s", options) )}' % (path [1:] or 'index', path, vue_path))
                    pathes.append (vue_path) # prefetch
            routes_list = ",\n ".join (routes)
            return routes_list, pathes

        global ROUTES_CACHE

        if not app.debug and base in ROUTES_CACHE:
            return ROUTES_CACHE [base]

        if "STATIC_PATH" in app.config:
            static_path = app.config.STATIC_ROOT
        else:
            static_path = os.path.join (app.home, 'static') # default

        current = os.path.join (static_path, VIEWS_DIR [1:], base [1:])
        routes_list, pathes = find (current)
        if not routes_list:
            home = os.path.join (os.path.dirname (__file__), '../static', VIEWS_DIR [1:], base [1:])
            routes_list, pathes = find (home)

        ROUTES_CACHE [base] = (routes_list, pathes)
        return routes_list, pathes

    # template filters --------------------------------------
    @app.template_filter ('vue')
    def vue (val):
        return '{{ %s }}' % val

    @app.template_filter ('summarize')
    def summarize (val, chars = 60):
        if not val:
            return ''
        s = val.find (" ", chars)
        if s == -1:
            return RX_SPACE.sub (" ", val.strip ())
        else:
            return RX_SPACE.sub (" ", val.strip () [: min (s, chars + 10)]) + '...'

    @app.template_filter ('attr')
    def attr (val):
        if not val:
            return '""'
        return '"{}"'.format (val.replace ('"', '\\"'))

    @app.template_filter ('upselect')
    def upselect (val, *names, **upserts):
        d = {}
        for k, v in val.items ():
            if k in names:
                d [k] = v
        d.update (upserts)
        return d

    @app.template_filter ('tojson_with_datetime')
    def tojson_with_datetime (data):
        return json.dumps (data, cls = ISODateTimeWithOffsetEncoder, ensure_ascii = False)


def __mount__ (app, mntopt):
    @app.route ('/base-template')
    def base_template (was):
        import atila_vue
        return f'<h1>Atila Vue Template {atila_vue.__version__}</h1>'
