#!/bin/bash

# Normally I would have the set -e here but rvm when loaded as function isn't compatible with set -e
#set -e

# if we have made it this far then we know that the
# plugin has already checked to see if both a Guardfile
# and a Gemfile exists. Therefore, we should be safe
# to assume that those two things exist in the provided
# project path.

function load_rvm_as_a_function() {
  # Here I load rvm as a bash function rather than a binary. I do
  # this because the binary version is limited and won't properly
  # create or switch to gemsets.
  #
  # For more information on binary/function mode of RVM refer to
  # the following url:  http://beginrescueend.com/workflow/scripting/
  if [[ -s "$HOME/.rvm/scripts/rvm" ]] ; then
    # First try to load from a user install
    source "$HOME/.rvm/scripts/rvm"
  elif [[ -s "/usr/local/rvm/scripts/rvm" ]] ; then
    # Then try to load from a root install
    source "/usr/local/rvm/scripts/rvm"
  else
    printf "ERROR: An RVM installation was not found.\n"
    return 1
  fi
  return 0
}

function run_guard() {
  printf "Running 'bundle exec guard'. All output/failures from this point on is from the 'bundle exec guard' command.\n\n"
  cd "$1" && bundle exec guard
}

echo "Starting Guard for $1"

load_rvm_as_a_function
if [ $? -ne 0 ]; then # failed to load rvm
  printf "Couldn't find or load RVM.\n"
  printf "Attempting to run Guard using your system gemset.\n"
  run_guard "$1"
else # successfully loaded rvm
  printf "Found and Successfully loaded RVM as a function.\n"
  if [ -e "$1/.rvmrc" ]; then # found project specific .rvmrc
    printf "Found an .rvmrc in the project directory. Trying to load it...\n"
   
    cd "$1"
    rvm rvmrc load "$1"
    if [ $? -ne 0 ]; then # failed to load project specific .rvmrc
      printf "Failed to load the project .rvmrc\n"
      printf "\nWE DID NOT RUN GUARD AS LOADING YOUR PROJECT SPECIFIC .rvmrc SHOULD NOT HAVE FAILED\n"
      return 1
    else # successfully loaded project specific .rvmrc
      printf "Successfully loaded the project .rvmrc\n"
      run_guard "$1"
    fi
  else # failed to find project specific .rvmrc
    printf "Failed to find a project specific .rvmrc in $1.\n"
    
    printf "Attempting to switch to default RVM enviornment.\n"
    rvm use default
    if [ $? -ne 0 ]; then # failed to switch to the users default gemset
      printf "Failed to switch to default RVM environment.\n"
      printf "\nWE DID NOT RUN GUARD AS SWITCHING TO YOUR DEFAULT RVM ENVIRONMENT SHOULD NOT HAVE FAILED\n"
      return 1
    else # successfully switched to the users default gemset
      printf "Successfully switched to your default RVM environment.\n"
      run_guard "$1"
    fi
  fi
fi

