Sublime Text 2 Guard Plugin
===========================

This project provides integration of Guard into the Sublime Text 2 editor. I wrote this as
a convenience tool to help improve my daily workflow while deving on numerous projects
using BDD and TDD.

This plugin provides an interface for controlling Guard and viewing Guards output within the
Sublime Text 2 editor. Not having to switch between a terminal and an editor to see Red/Green
states improves workflow drastically.


All of the commands are available via the command palette (**super+shift+p**).

When performing some normal operations in Sublime Text 2, like search,  it hides the Guard output.
Therefore, this plugin provides a default key binding (**super+shift+c**) to show or reshow the Guard output.

* Commands available when Guard is NOT running

    * Start Guard

* Commands available all of the time

    * Hide Guard Output
    * Show Guard Output (**super+shift+c**)

* Commands available when Guard IS running

    * Stop Guard
    * Run all Tests
    * Reload Guard
    * Toggle Notifications
    * Pause/Unpause
    * Output Help

## Installation

To install this Sublime Text 2 plugin, simply run the following commands:

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    git clone git://github.com/cyphactor/sublime_guard.git Guard

## Upgrade

To upgrade to the latest version, simply run the following commands:

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Guard
    git pull

## Usage

### Command Palette

As mentioned above the primary way of using this plugin is via the command palette (**super+shift+p**).
Once the command palette is up, fuzzy match the intendend command, and press the return key.

### Starting Guard

If Guard is not currently running, start Guard using the "Start Guard" command. It will bring up a pane at
the bottom of the screen and show the output of Guard as it runs.

### Show/Hide Guard Output

The Guard output can be shown and hidden using the "Show Guard Output" and "Hide Guard Output" command respectively.
The "Show Guard Output" command is also available via the default key binding (**super+shift+c**).

### Other Useful Commands

A few of my favorites commands are "Run all Tests", "Reload Guard", and "Pause/Unpause". The
"Run all Tests" command will simply request that Guard run all of the tests. The "Reload Guard" command
is useful if changes have been made to Rails config initializers or something else that requires reloading. The
"Pause/Unpause" command is primarily useful when switching branches or rebasing. It will
temporarily prevent Guard from monitoring the project files for changes.

## RVM Support

This plugin supports RVM out of the box. Basically, it means that it first checks to see if RVM is installed and loads it.
Once RVM is loaded it then looks to see if any of the top level folders in Sublime Text 2 contain a project specific .rvmrc. If one does it will
load that .rvmrc and attempt to run Guard on that project.

In the case where it can't find RVM it simply tries to run Guard assuming it is installed as a system gem.

## FAQs

#### Does the Guard process die/exit when Sublime Text 2 dies/exits?

Yes.

#### Why would I get "Failed to find Guardfile and Gemfile in any of the open folders." as an error?

This error message is a result of the project currently loaded in Sublime Text 2 missing either the Guardfile, the Gemfile, or both.
Currently, this plugin requires a Guardfile and a Gemfile to be present in the projects root path to run Guard.

#### Where do I find out about Guardfiles?

The best place to find out about Guardfiles is the [Guard project page](http://github.com/guard/guard).

#### Where do I found out about Gemfiles?

The best place to find out about Gemfiles is the [Bundler project](http://gembundler.com/).

#### What do I do if I find a bug?

Please report all bugs/issues via the [Issues](http://github.com/cyphactor/sublime_guard/issues) tab.

#### What do I do if I have an idea for a feature/change?

All feature requests or change requests should be made via the [Issues](http://github.com/cyphactor/sublime_guard/issues) tab.

## Contributions

As with all of my Open Source Projects I am open to contributions. There are numerous ways one can contribute.

1. **Contribute Code/Documentation** - If you would like to contribute code or documentation changes please fork the repository and submit a pull request.
2. **Feature Requests/Bug Reports** - If you would like to contribute by submitting either a feature request or a bug report you may do so via the [Issues](http://github.com/cyphactor/sublime_guard/issues) tab.