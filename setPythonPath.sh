#!/bin/bash

#set the Pythonpath so Python will recognize the CodeKlaviever package
#run this script everytime you start a new shell session
#alternatively: put it in your ~/bashrc
#TODO: find options for windows users

PYTHONPATH=$(pwd)'/CodeKlavier':$PYTHONPATH
export PYTHONPATH
