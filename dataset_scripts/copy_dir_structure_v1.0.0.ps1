############################################################################################
# Author: Daniel Mendes
# Date: 11/30/23
# Class: CS 46x - Capstone Project
# Group: Child AI (Tentative Name)
# Description:
#   This is a basic PowerShell script used to copy the file structure of one directory
#   into a second directory. This is just a helper script that must be run before the
#   auto-synthesis script actually works. 
# Version: 1.0.0 
############################################################################################

$source='TYPE PATH HERE'
$dest='TYPE PATH HERE'


robocopy $source $dest /e /xf *.*

$source='TYPE PATH HERE'
$dest='TYPE PATH HERE'

robocopy $source $dest /e /xf *.*