#!/bin/bash

# This scripts job is to take the GuardOutput.tmLanguage and
# GuardOutput.tmTheme out of the development repository and use them to either
# create or update a the sublime_guard TextMate bundle. This is necessary
# because it is much easier to test/develop the tmLanguage and tmTheme files in
# TextMate's Bundle Editor.

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
_tm_bundle_skel_path="${_script_base_path}sublime_guard_tmbundle_skel"
echo "Creating/Updating TextMate bundle skeleton at ${_tm_bundle_path}"
if [ ! -d "${_tm_bundle_path}" ]; then
  mkdir "${_tm_bundle_path}"
fi

echo "Copying bundle skelton contents over..."
cp -r "${_tm_bundle_skel_path}/" "${_tm_bundle_path}"

echo "Copying GuardOutput.tmLanguage to TextMate bundle..."
cp "${_script_base_path}../GuardOutput.tmLanguage" "${_tm_bundle_path}/Syntaxes/GuardOutput.tmLanguage"

echo "Copying GuardOutput.tmTheme to TextMate themes directory..."
cp "${_script_base_path}../GuardOutput.tmTheme" "${_tm_themes_path}/"

echo "Finished pushing theme to TextMate!"
