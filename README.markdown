Sublime Text 2 Guard Plugin
===========================

This project provides integration of Guard into the Sublime Text 2 editor. I wrote this as
a quick fun project to help improved my daily workflow while deving on numerous projects
using BDD and TDD.

This plugin basically makes it so that you don't have to leave your Sublime Text 2 editor to
get the benefits that Guard normally provides, see the output of Guard as it runs tests, or
control Guard as you would normally be able to.

This plugin does NOT include any default key bindings. In fact I do not recommend that you
setup key bindings for this plugin. This plugin simply provides the following commands
through the commands popup menu (Cmd+Shift+P):

* Commands available when Guard is NOT running

    * Start Guard

* Commands available all of the time

    * Hide Guard Output
    * Show Guard Output

* Commands available when Guard IS running

    * Stop Guard
    * Run all Tests
    * Reload Guard
    * Toggle Notifications
    * Pause
    * Output Help

## Installation

Installing this Sublime Text 2 plugin follows the same process you would use to install any other Sublime Text 2 plugin. Simply run the following commands:

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    git clone git://github.com/cyphactor/sublime_guard.git Guard

## Upgrade

If you have already installed this plugin to upgrade to the latest version you should simply have to run the following commands:

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Guard
    git pull

## Usage

### Commands Popup Menu

As mentioned above the standard way of using this plugin is via the commands popup menu (**Cmd+Shift+P**).
Once the commands popup menu is up and you fuzzy match the command you want to run simply select it or
press the return key with it highlighted.

### Starting Guard

If Guard is not currently running you probably want to "Start Guard" first. When you run the "Start Guard"
command it will bring up a pane at the bottom of the screen and show you the output of Guard as it runs.

### Show/Hide Guard Output

You can Hide and Show this output pane at any time using the "Hide Guard Output" and "Show Guard Output"
commands.

### Other Useful Commands

Beyond the above the "Run all Tests", "Reload Guard", and "Pause" commands are a few of my favorite. The
"Run all Tests" command will simply request that Guard run all of the tests. The "Reload Guard" command
is useful if you have changed some Rails config initializers or something that requires reloading. The
"Pause" command is primarily useful when you are going checkout a different branch, rebase, etc. It will
prevent Guard from running all kinds of tests as things are in the process of changing.

## Contributions

As with all of my Open Source Projects I am open to contributions. There are numerous ways one can contribute
below is are just a few.

1. **Contribute Code/Documentation** - If you would like to contribute code or documentation changes please fork the repository and submit a pull request.
2. **Feature Requests/Bug Reports** - If you would like to contribute by submitting either a feature request or a bug report you may do so via the [Issues](http://github.com/cyphactor/sublime_guard/issues) tab.