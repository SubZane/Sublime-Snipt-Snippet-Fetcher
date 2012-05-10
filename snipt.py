import sublime, sublime_plugin, urllib2, json, os, re

class SyncSniptCommand(sublime_plugin.TextCommand):

    def get_userinfos(self):
        # snipt plugin settings
        self.settings = sublime.load_settings("Snipt.sublime-settings")
        self.username = self.settings.get('snipt_username')
        self.apikey = self.settings.get('snipt_apikey')
        self.userid = self.settings.get('snipt_userid')

        if (not self.apikey):
            sublime.error_message('No snipt.net apikey. You must first set you apikey in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
            return
        
        if (not self.userid):
            sublime.error_message('No snipt.net userid. You must first set you userid in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
            return
        
        if (not self.username):
            sublime.error_message('No snipt.net username. You must first set you username in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
            return

    def run(self, edit):
        # check for userinfos config
        self.get_userinfos()
        username = self.username
        apikey = self.apikey
        userid = self.userid
      
        # grab the user data
        try:
            response = urllib2.urlopen('https://snipt.net/api/public/snipt/?user={0}'.format(userid))
            #for private API
            #response = urllib2.urlopen('https://snipt.net/api/public/snipt/?username={0}&api_key={1}&format=json'.format(username, apikey))
        except urllib2.URLError, (err):
            sublime.error_message("Connection refused. Try again later. Snipt step: 1"+err)
            return
            
        # grab all user snipt #'s
        parse = json.load(response)
        parse_me = parse['objects']

        # run the loop
        for item in parse_me:
            title = item['title']
            code = item['code']
             
            rx = re.compile('\W+')
            cleantitle = rx.sub(' ', title).strip()

            # lets turn wine (snipts) into water (sublime snippets)
            buildfile = 'repo/{0}.sublime-snippet'.format(cleantitle[0:20])
            newfile = open(buildfile,'w+')
            newfile.write('<snippet><content><![CDATA[{0}]]></content><tabTrigger>snipt</tabTrigger></snippet>'.format(code))
            newfile.close()

# This is coming soon. Ability to send text to snipt.net and create a sublime snippet.
# class CreateSniptCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         print 1