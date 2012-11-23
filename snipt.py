import sublime, sublime_plugin, urllib2, json, os, re

SETTINGS = sublime.load_settings("Snipt.sublime-settings")
USERNAME = SETTINGS.get('snipt_username')
APIKEY = SETTINGS.get('snipt_apikey')
USERID = SETTINGS.get('snipt_userid')
APIMODE = SETTINGS.get('snipt_apimode')
SEARCHLIMIT = 15

if (not APIMODE):
    sublime.error_message('No snipt.net apimode. You must first set you API mode in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
if (APIMODE == "public"):
    if (not USERID):
        sublime.error_message('No snipt.net userid. You must first set you userid in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
elif (APIMODE == "private"):
    if (not USERNAME):
        sublime.error_message('No snipt.net username. You must first set you username in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
    if (not APIKEY):
        sublime.error_message('No snipt.net apikey. You must first set you apikey in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')



def get_lexers():
    try:
        response = urllib2.urlopen('https://snipt.net/api/public/lexer/')
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    lexers = parse['objects']
    return lexers

def get_private_snippets(tag):
    global USERNAME, APIKEY
    try:
        if tag == None:
            response = urllib2.urlopen('https://snipt.net/api/private/snipt/?username={0}&api_key={1}&format=json'.format(USERNAME, APIKEY))
        else:
            response = urllib2.urlopen('https://snipt.net/api/private/snipt/?username={0}&api_key={1}&format=json&tag={2}'.format(USERNAME, APIKEY, tag))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    snippets = parse['objects']
    return snippets

def get_favorite_private_snippets():
    global USERNAME, APIKEY
    try:
        response = urllib2.urlopen('https://snipt.net/api/private/favorite/?username={0}&api_key={1}&format=json'.format(USERNAME, APIKEY))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    uris = parse['objects']
    return snippets

def get_public_snippets(tag):
    global USERID
    try:
        if tag == None:
            response = urllib2.urlopen('https://snipt.net/api/public/snipt/?user={0}'.format(USERID))
        else:
            response = urllib2.urlopen('https://snipt.net/api/public/snipt/?tag={0}&limit={1}'.format(tag, SEARCHLIMIT))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    snippets = parse['objects']
    return snippets

def find_public_snippets(keyword):
    global SEARCHLIMIT
    try:
        response = urllib2.urlopen('https://snipt.net/api/public/snipt/?format=json&q={0}&limit={1}'.format(keyword, SEARCHLIMIT))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    snippets = parse['objects']
    return snippets

def get_private_tags():
    global USERNAME, APIKEY
    try:
        response = urllib2.urlopen('https://snipt.net/api/private/tag/?username={0}&api_key={1}&format=json'.format(USERNAME, APIKEY))
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    tags = parse['objects']
    return tags

def get_public_tags():
    global USERNAME, APIKEY
    try:
        response = urllib2.urlopen('https://snipt.net/api/public/tag/')
    except urllib2.URLError, (err):
        sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
        return
        
    parse = json.load(response)
    tags = parse['objects']
    return tags

def find_private_snippets_by_tag(tag):
    snippets = get_private_snippets(tag['id'])
    snippet_names = [snippet['title'] for snippet in snippets]
    def on_snippet_num(num):
        if num != -1:
            insert_selected_snippet(snippets[num])
    sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)

def find_public_snippets_by_tag(tag):
    snippets = get_public_snippets(tag['id'])
    snippet_names = [snippet['title'] for snippet in snippets]
    def on_snippet_num(num):
        if num != -1:
            insert_selected_snippet(snippets[num])
    sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)

def find_private_snippets_by_lexer(lexer):
    view = sublime.active_window().active_view()
    edit = view.begin_edit()
    for region in view.sel():
        view.replace(edit, region, snippet['code'])
    view.end_edit(edit) 

def insert_selected_snippet(snippet):
    #    title = item['title']
    #    code = item['code']
    view = sublime.active_window().active_view()
    edit = view.begin_edit()
    for region in view.sel():
        view.replace(edit, region, snippet['code'])
    view.end_edit(edit) 


class ShowLexers(sublime_plugin.TextCommand):

    def run(self, edit):
        lexers = get_lexers()
        lexer_names = [lexer['name'] for lexer in lexers]
        def on_lexer_num(num):
            if num != -1:
                insert_selected_snippet(snippets[num])
        sublime.active_window().show_quick_panel(lexer_names, on_lexer_num)

class SearchPublicSnipts(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.active_window().show_input_panel("Enter keyword:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        snippets = find_public_snippets(text)
        snippet_names = [snippet['title'] for snippet in snippets]
        def on_snippet_num(num):
            if num != -1:
                insert_selected_snippet(snippets[num])
        sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)

class GetPublicSniptsByTagCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        tags = get_public_tags()
        tag_names = [tag['name'] for tag in tags]
        def on_tag_num(num):
            if num != -1:
                find_public_snippets_by_tag(tags[num])
        sublime.active_window().show_quick_panel(tag_names, on_tag_num)

class InsertPrivateSniptsByTagCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        tags = get_private_tags()
        tag_names = [tag['name'] for tag in tags]
        def on_tag_num(num):
            if num != -1:
                find_private_snippets_by_tag(tags[num])
        sublime.active_window().show_quick_panel(tag_names, on_tag_num)

class InsertFavoritePrivateSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        snippets = get_favorite_private_snippets()
        snippet_names = [snippet['title'] for snippet in snippets]
        def on_snippet_num(num):
            if num != -1:
                insert_selected_snippet(snippets[num])
        sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)

class InsertPrivateSniptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        snippets = get_private_snippets(None)
        snippet_names = [snippet['title'] for snippet in snippets]
        def on_snippet_num(num):
            if num != -1:
                insert_selected_snippet(snippets[num])
        sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)
