#   ------------------------------------------------------------
#   Snipt.net Snippet Fetcher
#   Version 1.1
#   by Andreas Norman (@andreasnorman)
#
#   https://github.com/SubZane/Sublime-Snipt.net
#
#   ------------------------------------------------------------

import sublime, sublime_plugin, urllib2, json, os, re

SETTINGS = sublime.load_settings("Snipt.sublime-settings")

BASEPATH = sublime.packages_path()+'/Snipt.net Snippet Fetcher/'

USERNAME = SETTINGS.get('snipt_username')
APIKEY = SETTINGS.get('snipt_apikey')
OTHER_USERS = SETTINGS.get('snipt_other_users')
OTHER_USER_IDS = load_other_users()

PRIVATE_SNIPPETS = BASEPATH+'snippets.private.json'
PUBLIC_SNIPPETS = BASEPATH+'snippets.public.[userid].json'
FAVORITE_SNIPPETS = BASEPATH+'snippets.favorite.json'

if (not USERNAME):
    sublime.error_message('No snipt.net username. You must first set you username in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings')
else:
    USERID = get_user_id(USERNAME)
if (not APIKEY):
    sublime.error_message('No snipt.net apikey. You must first set you apikey in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings')

def load_other_users_into_list():
    global OTHER_USERS
    userlist = [users.strip() for users in OTHER_USERS.split(',')]
    return userlist

def load_other_users():
    global OTHER_USERS
    user_ids = [get_user_id(users.strip()) for users in OTHER_USERS.split(',')]
    return user_ids

def get_user_id(username):
    try:
        response = urllib2.urlopen('https://snipt.net/api/public/user/?username={0}'.format(username))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
    parse = json.load(response)
    try:
        user_id = parse['objects'][0]['id']
    except Exception, e:
        print "User not found: "+str(e)
        return 0
    return user_id

def get_public_snippets(username):
    global USERID
    try:
        if username == None:
            response = urllib2.urlopen('https://snipt.net/api/public/snipt/?user={0}'.format(USERID))
        else:
            user_id = get_user_id(username)
            response = urllib2.urlopen('https://snipt.net/api/public/snipt/?user={0}'.format(user_id))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    snippets = parse['objects']
    return snippets

def cache_public_snippets(username):
    global USERID, PUBLIC_SNIPPETS
    if username == None:
        user_id = USERID
    else:
        user_id = get_user_id(username)
    
    snippet_file_name = PUBLIC_SNIPPETS.replace("[userid]", str(user_id));
    try:
        response = urllib2.urlopen('https://snipt.net/api/public/snipt/?user={0}'.format(user_id))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
    snippetdata = response.read()
    try:   
        newfile = open(snippet_file_name,'w+')
        newfile.write(snippetdata)
        newfile.close()
    except IOError, (err):
        sublime.error_message("Cannot create or write to file: "+str(err))
        return
    return

def get_cached_public_snippets(username):
    global PUBLIC_SNIPPETS, USERID
    if username == None:
        user_id = USERID
    else:
        user_id = get_user_id(username)

    snippet_file_name = PUBLIC_SNIPPETS.replace("[userid]", str(user_id));

    if os.path.isfile(snippet_file_name) == False:
        cache_public_snippets(username)

    filedata=open(snippet_file_name)

    try:
        parse = json.load(filedata)
    except Exception, (err):
        sublime.error_message("No snippets found. Try adding some. "+str(err))

    snippets = parse['objects']
    return snippets

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

class InsertPublicSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        snippets = get_cached_public_snippets(None)
        show_snippets_quick_panel(snippets)

class InsertOtherUserSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        userlist = load_other_users_into_list()
        def on_user(num):
            if num != -1:
                snippets = get_cached_public_snippets(userlist[num])
                show_snippets_quick_panel(snippets)
        sublime.active_window().show_quick_panel(userlist, on_user)

def show_snippets_quick_panel(snippets_data):
    if snippets_data == None:
        message_dialog("No snippets found")
    else:
        snippet_names = [snippet['title'] for snippet in snippets_data]
        def on_snippet_num(num):
            if num != -1:
                insert_selected_snippet(snippets_data[num])
        sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)

class CacheAllSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cache_private_snippets()
        cache_favorite_snippets()
        cache_public_snippets(None)
        userlist = load_other_users_into_list()
        for user in userlist:
            cache_public_snippets(user)