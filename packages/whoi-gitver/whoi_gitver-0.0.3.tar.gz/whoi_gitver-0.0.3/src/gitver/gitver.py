#!/bin/python3
import subprocess
import os
import sys

MIN_PYTHON = (3, 7)


def getVer(fileDir):
    # Check for minimum python version
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

    # Check that we are even in a git repository
    if (subprocess.call(["git", "branch"],cwd=fileDir, stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) != 0):
        sys.exit("Error: not in a git repository")


    # Get the project name, either from the remote url or from the local directory
    result = subprocess.run(["git", "remote"],cwd=fileDir, capture_output=True, text=True)
    remotes = result.stdout.splitlines()

    # First check if there are no remotes, in that case, use dirname
    if  not remotes:
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=fileDir,capture_output=True, text=True)
        project_name = os.path.splitext(os.path.basename(result.stdout.rstrip()))[0]
    # Then check if origin in remotes
    elif "origin" in remotes:
        result = subprocess.run(["git", "config", "--get", "remote.origin.url"],cwd=fileDir, capture_output=True, text=True)
        project_name = os.path.splitext(os.path.basename(result.stdout.rstrip()))[0]
    # Otherwise, report an error because I haven't decided what to do here
    else:
        sys.exit("Error: Could not determine project name from repository. No remote origin")


    #Get the current branch name
    result = subprocess.run(["git", "branch", "--show-current"], cwd=fileDir,capture_output=True, text=True)
    branch = result.stdout.rstrip()

    # Get the version
    result = subprocess.run(["git", "describe", "--tags"],cwd=fileDir, capture_output=True, text=True)
    tag = result.stdout.rstrip()

    result = subprocess.run(["git", "describe", "--tags", "--always"],cwd=fileDir, capture_output=True, text=True)
    ver = result.stdout.rstrip()

    # In case there are no tags, we will default to v0.0.0 as a placeholder
    if not tag:
        ver = "v0.0.0-" + ver

    verstr = project_name + "_" + branch + "_" + ver

    # Check if we need to append the dirty or local flag
    dirty = False
    local = False

    result = subprocess.run(["git", "rev-list", "--count", "origin/" + branch + ".." + branch],cwd=fileDir, capture_output=True, text=True)
    if result.stdout:
        #print(len(result.stdout))
        ncommits = int(result.stdout.rstrip())
    else:
        ncommits = 0

    if ncommits > 0:
        local = True

    result = subprocess.run(["git", "status", "--porcelain"],cwd=fileDir, capture_output=True, text=True)
    status = result.stdout

    for line in status.splitlines():
        if line.startswith(" M"): # Check for file with modifications
            dirty = True
        if line.startswith("??"): # Check for a file that has not been added to version control
            dirty = True

    if dirty:
        verstr = verstr + "-dirty"
    elif local:
        verstr = verstr + "-local"

    return(verstr)
