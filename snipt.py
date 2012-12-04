import sublime, sublime_plugin, urllib2, json, os, re

SETTINGS = sublime.load_settings("Snipt.sublime-settings")

BASEPATH = sublime.packages_path()+'/Snipt.net Snippet Fetcher/'

USERNAME = SETTINGS.get('snipt_username')
APIKEY = SETTINGS.get('snipt_apikey')
USERID = SETTINGS.get('snipt_userid')
APIMODE = SETTINGS.get('snipt_apimode')

PRIVATE_SNIPPETS = BASEPATH+'snippets.private.json'
FAVORITE_SNIPPETS = BASEPATH+'snippets.favorite.json'

if (not APIMODE):
    sublime.error_message('No snipt.net apimode. You must first set you API mode in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings')
if (APIMODE == "public"):
    if (not USERID):
        sublime.error_message('No snipt.net userid. You must first set you userid in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings')
elif (APIMODE == "private"):
    if (not USERNAME):
        sublime.error_message('No snipt.net username. You must first set you username in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings')
    if (not APIKEY):
        sublime.error_message('No snipt.net apikey. You must first set you apikey in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings')

def get_private_snippets(tag):
    global USERNAME, APIKEY
    try:
        if tag == None:
            response = urllib2.urlopen('https://snipt.net/api/private/snipt/?username={0}&api_key={1}&format=json'.format(USERNAME, APIKEY))
        else:
            response = urllib2.urlopen('https://snipt.net/api/private/snipt/?username={0}&api_key={1}&format=json&tag={2}'.format(USERNAME, APIKEY, tag))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+str(err))
        return
        
    parse = json.load(response)
    snippets = parse['objects']
    return snippets

def get_cached_private_snippets():
    global PRIVATE_SNIPPETS
    if os.path.isfile(PRIVATE_SNIPPETS) == False:
        cache_private_snippets()

    filedata=open(PRIVATE_SNIPPETS)

    try:
        parse = json.load(filedata)
    except Exception, (err):
        sublime.error_message("No snippets found. Try adding some. "+str(err))

    snippets = parse['objects']
    return snippets

def get_cached_favorite_snippets():
    global FAVORITE_SNIPPETS
    if os.path.isfile(FAVORITE_SNIPPETS) == False:
        cache_favorite_snippets()

    filedata=open(FAVORITE_SNIPPETS)

    try:
        parse = json.load(filedata)
    except Exception, (err):
        sublime.error_message("No favorite snippets found. Try adding some.")

    snippets = parse['objects']
    return snippets

def cache_private_snippets():
    global USERNAME, APIKEY, PRIVATE_SNIPPETS
    try:
        response = urllib2.urlopen('https://snipt.net/api/private/snipt/?username={0}&api_key={1}&format=json'.format(USERNAME, APIKEY))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
    snippetdata = response.read()
    try:   
        newfile = open(PRIVATE_SNIPPETS,'w+')
        newfile.write(snippetdata)
        newfile.close()
    except IOError, (err):
        sublime.error_message("Cannot create or write to file: "+str(err))
        return
    return

def cache_favorite_snippets():
    global FAVORITE_SNIPPETS

    favorites = get_favorite_private_snippets()

    try:   
        newfile = open(FAVORITE_SNIPPETS,'w+')
        newfile.write(favorites)
        newfile.close()
    except IOError, (err):
        sublime.error_message("Cannot create or write to file: "+str(err))
        return
    return

def get_favorite_private_snippets():
    global USERNAME, APIKEY
    try:
        response = urllib2.urlopen('https://snipt.net/api/private/favorite/?username={0}&api_key={1}&format=json'.format(USERNAME, APIKEY))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+str(err))
        return
        
    parse = json.load(response)
    favorites = parse['objects']
    snippetstring = ''
    for favorite in favorites:
        snippet = get_snippet_by_uri(favorite['snipt'])
        if snippetstring == '':
            snippetstring = snippet
        else:
            snippetstring += ', '+ snippet
    snippets = '{0}"objects": [{1}]{2}'.format("{",snippetstring,"}")
    return snippets

def get_snippet_by_uri(uri):
    try:
        response = urllib2.urlopen('https://snipt.net{0}'.format(uri))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+str(err))
        return
    parse = json.load(response)
    snippet = json.dumps(parse)

    return snippet

def insert_selected_snippet(snippet):
    view = sublime.active_window().active_view()
    edit = view.begin_edit()
    for region in view.sel():
        view.replace(edit, region, snippet['code'])
    view.end_edit(edit) 

class InsertFavoriteSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        snippets = get_cached_favorite_snippets()
        show_snippets_quick_panel(snippets)

class InsertPrivateSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        snippets = get_cached_private_snippets()
        show_snippets_quick_panel(snippets)

def show_snippets_quick_panel(snippets_data):
    if snippets_data == None:
        message_dialog("No snippets found")
    else:
        snippet_names = [snippet['title'] for snippet in snippets_data]
        def on_snippet_num(num):
            if num != -1:
                insert_selected_snippet(snippets_data[num])
        sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)

class CachePrivateSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cache_private_snippets()
        cache_favorite_snippets()