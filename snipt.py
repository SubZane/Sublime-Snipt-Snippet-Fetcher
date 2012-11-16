import sublime, sublime_plugin, urllib2, json, os, re

class ListSniptsCommand(sublime_plugin.TextCommand):
    def get_userinfos(self):
        # snipt plugin settings
        self.settings = sublime.load_settings("Snipt.sublime-settings")
        self.username = self.settings.get('snipt_username')
        self.apikey = self.settings.get('snipt_apikey')
        self.userid = self.settings.get('snipt_userid')
        self.apimode = self.settings.get('snipt_apimode')

        if (not self.apimode):
            sublime.error_message('No snipt.net apimode. You must first set you API mode in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
            return

        if (self.apimode == "public"):
            if (not self.userid):
                sublime.error_message('No snipt.net userid. You must first set you userid in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
                return
        elif (self.apimode == "private"):
            if (not self.username):
                sublime.error_message('No snipt.net username. You must first set you username in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
                return
            if (not self.apikey):
                sublime.error_message('No snipt.net apikey. You must first set you apikey in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
                return

    def get_snippets(self):
        # check for userinfos config
        self.get_userinfos()
        username = self.username
        apikey = self.apikey
        userid = self.userid
        apimode = self.apimode

        # grab the user data
        try:
            if (apimode == "public"):
                response = urllib2.urlopen('https://snipt.net/api/public/snipt/?user={0}'.format(userid))
            else:
                response = urllib2.urlopen('https://snipt.net/api/private/snipt/?username={0}&api_key={1}&format=json'.format(username, apikey))
        except urllib2.URLError, (err):
            sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
            return
            
        # grab all user snipt #'s
        parse = json.load(response)
        snippets = parse['objects']

        snippet_names = [snippet['title'] for snippet in snippets]
        def on_snippet_num(num):
            if num != -1:
                self.handle_snipt(snippets[num])

        sublime.active_window().show_quick_panel(snippet_names, on_snippet_num)
        
        #    title = item['title']
        #    code = item['code']

    def handle_snipt(self, snippet):
        edit = self.view.begin_edit()
        # insert the correct code here, but dunno how yet :P
        view = sublime.active_window().active_view()
        edit = view.begin_edit()
        for region in view.sel():
            view.replace(edit, region, snippet['code'])
        view.end_edit(edit) 
    
    def run(self, edit):
        self.get_snippets()
