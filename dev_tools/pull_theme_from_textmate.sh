#!/bin/bash

# This scripts job is to pull the GuardOutput.tmLanguage and
# GuardOutput.tmTheme files out of TextMate and copy them back into the source
# tree. This script is intended to be used when you have made some changes to
# the GuardOutput.tmLanguage and GuardOutput.tmTheme files via the TextMate
# Bundle Editor and you want to bring those changes back into the source
# repository.

set -e

_bundle_name="sublime_guard.tmbundle"

_script_name=`basename $0`
if [ "`echo $0 | cut -c1`" = "/" ]; then
  _script_base_path=`dirname $0`
else
  _script_base_path=`pwd`/`echo $0 | sed -e s/${_script_name}//`
fi

_tm_bundle_path="${HOME}/Library/Application Support/TextMate/Bundles/${_bundle_name}"
_tm_themes_path="${HOME}/Library/Application Support/TextMate/Themes"

echo "Copying GuardOutput.tmLanguage from TextMate bundle to source tree..."
cp "${_tm_bundle_path}/Syntaxes/GuardOutput.tmLanguage" "${_script_base_path}../GuardOutput.tmLanguage"

echo "Copying GuardOutput.tmTheme from TextMate themes directory to source tree..."
cp "${_tm_themes_path}/GuardOutput.tmTheme" "${_script_base_path}../GuardOutput.tmTheme"

echo "Finished pulling theme from TextMate into source tree!"
