#Snipt Snippet Fetcher
Version 1.1

## Description
Forked from [Taecho/Sublime-Snipt](https://github.com/Taecho/Sublime-Snipt)

This Sublime Text 2 Plugin enables you to reach the snippets on Snipt.net
* Browse and insert your own public and private snippets
* Browse and insert your favorite snippets
* Browse and insert public snippets from your friends (provide usernames in the settings)
* Local cache for all snippets to improve access speed

## Installation
### Using Git
Go to your Sublime Text 2 Packages directory and clone the repository using the command below:

    git clone https://github.com/SubZane/Sublime-Snipt.net

### Download Manually

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to `Snipt.net Snippet Fetcher`
* Rename the folder to `Snipt.net Snippet Fetcher` (This is very important)
* Copy the folder to your Sublime Text 2 `Packages` directory

## Settings
Find the settings file in the menu: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt.net Snippet Fetcher ~> Settings
* `snipt_username` This is your username on Snipt.net
* `snipt_apikey` This is your API key on Snipt.net
* `snipt_other_users` This is a comma delimted list of other usernames. This enables you to access other users snippets.

## How to use
* Launch the Command Palette using the menu (Tools->Command Palette...) or short key-command Shift+Cmd+P
* Find the prefix `Snipt Snippet Fetcher:`
* `Snipt Snippet Fetcher: Cache All Snippets` will cache all snippets locally in a json file.
* `Snipt Snippet Fetcher: Insert Private snippet` will use the cached json file to help you insert your private snippets. This function will cache if no cache found.
* `Snipt Snippet Fetcher: Insert Favorite snippet` will use the cached json file to help you insert your favorite snippets. This function will cache if no cache found.
* `Snipt Snippet Fetcher: Insert Public snippet` will use the cached json file to help you insert your public snippets. This function will cache if no cache found.
* `Snipt Snippet Fetcher: Insert Other Users Snippets` will use the cached json file to help you insert a public snippet from another user. This function will cache if no cache found.

## To-do's
* Ability to create new snippets

## Authors
Twitter: [Andreas Norman](http://www.twitter.com/andreasnorman) GitHub: [SubZane](https://github.com/SubZane)
