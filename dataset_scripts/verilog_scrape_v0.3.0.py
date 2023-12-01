############################################################################################
# Author: Daniel Mendes
# Date: 11/30/23
# Class: CS 46x - Capstone Project
# Group: Child AI (Tentative Name)
# Description:
#   This file is used to extract the Verilog files from all of the open-license repositories
#   listed in the Verilog Autocompletion project by Enrique Deharne, linked below:
#       (https://github.com/99EnriqueD/verilog_autocompletion/)
#   All of the GitHub repositories specified in a CSV file are cloned. Afterwards, all
#   files are removed EXCEPT for Verilog files (ending in the extension '.v'). Additional
#   metadata about the repositories is thrown away, but can be written to files if needed.
#   
#   Files downloaded this way could be checked against the "deduplicated file index" in 
#   order to reduce redudancy in the dataset, but that isn't being done in this version. 
# Version: 0.3.0 
############################################################################################

import csv
import sys
import git #GitPython used to clone repos 
from glob import glob #Glob used to recursively travel through files to grab the verilog ones only
import shutil #shutil used to recursively copy all verilog files + delete the cloned github repos 
from pathlib import Path
import os

############################################################################################
#
# CHANGE CONSTANTS BELOW
# FOR THE DIRECTORY PATHS, SPECIFY DIRECTORIES WITHOUT THE FINAL "\" 
#
############################################################################################

# Change this to the target path of a temporary directory for cloning all the github repos
TEMP_REPO_PATH = r"TYPE PATH HERE"

# Change this to the target path of a directory where the Verilog files will be stored
#   This path PRESERVES the original repo file structure 
S_VERILOG_PATH = r"TYPE PATH HERE"

# Change this to the target path of a directory where the Verilog files will be stored
#   This path DOESN'T PRESERVE the original repo file structure 
U_VERILOG_PATH = r"TYPE PATH HERE"

# Change this to the path of your "permissive_all_deduplicated_repos.csv" file
REPO_CSV_PATH = r"TYPE PATH HERE"

# Change this to the path of your "filtered_near_deduplicated_file_index.csv" file
#   CURRENTLY NOT USED
DEDUP_CSV_PATH = r"TYPE PATH HERE"

# The number of repos cloned
#   Set to 0 to download EVERYTHING
REPO_PARSE_COUNT = 5

############################################################################################
#
# DO NOT CHANGE ANY CODE BELOW
#
############################################################################################

#Opens the "permissive_all_deduplicated_repos.csv" file to download all repos inside
def clone_verilog_repos(in_path):
    with open(in_path, encoding='utf8') as inf:
        reader = csv.reader(inf)
        counter = 0 # Temp counter for testing 

        next(inf) #Skip first line of CSV
        for line in reader:
            counter += 1 #Temp
            
            #Grabs all metadata about the repos
            #   NOT ALL INFO IS GRABBED/USED ATM
            repo_url = line[1]
            repo_date = line[2]
            repo_desc = line[3]
            fork_count = line[4]
            repo_full_name = line[5]
            repo_lan = line[6]
            repo_name = line[8]
            repo_size = line[9]

            curr_path = TEMP_REPO_PATH + '/' + repo_name

            #Skip arbitrarily large repository
            if (int(repo_size) > 50000): 
                continue

            #Clones the repository to a temporary location
            curr_path = TEMP_REPO_PATH + '/' + repo_name
           #repo = git.Repo.clone_from(repo_url, curr_path, branch='master')
            try:
                repo = git.Repo.clone_from(repo_url, curr_path)
            except Exception as e:
                print("Issue with repo: " + repo_name)
                print(e)

            #Grabs only the verilog files, then deletes the repository folder
            isolate_verilog_files(repo_name)
            isolate_verilog_files_wfstructure(repo_name)

            #WINDOWS ISSUE: Read-only files can't be deleted with shutil.rmtree
            #   This has some issues with the github files here
            #   I haven't been able to fix this so I just use a powershell script to run the python script + delete the folders lol
            #   If someone else gets this to work that would be great
            '''
            full_perms = 0o777
            for filename in glob(curr_path + "/**", recursive=True):
                print(filename)
                os.chmod(filename, full_perms)
            shutil.rmtree(curr_path)
            '''
            
            #TEMP, only tries X repos right now
            if (counter == REPO_PARSE_COUNT): 
                break  
        
        inf.close() 


#Deletes every non-verilog file
#   Does NOT preserve repo file structure
def isolate_verilog_files(repo_name):
    #Pattern matching all folders inside the given repository
    verilog_search_path = TEMP_REPO_PATH + "/" + repo_name + "/**/*.v"

    
    out_path = U_VERILOG_PATH + "/" + repo_name
    for filename in glob(verilog_search_path, recursive=True):
        Path(out_path).mkdir(parents=True, exist_ok=True,mode=0o777) #Maybe change mode?
        
        #Removes everything but the filename
        nopath_fname = os.path.basename(filename)
        
        #Copies to the target path
        outpath_withf = out_path + "/" + nopath_fname
        shutil.copyfile(filename, outpath_withf)


#Deletes every non-verilog file
#   BUT, also maintains file structure in case it's useful
def isolate_verilog_files_wfstructure(repo_name):
    #Pattern matching all folders inside the given repository
    verilog_search_path = TEMP_REPO_PATH + "/" + repo_name + "/**/*.v"
    
    out_path = S_VERILOG_PATH + "/"
    for filename in glob(verilog_search_path, recursive=True):
        #Removes the temp filepath
        semi_path_fname = filename.replace(TEMP_REPO_PATH, "")
   
        outpath_withf = out_path + semi_path_fname

        #Create the path/file, then perform the copy
        #   Need to make the parent since we have the actual filename now
        Path(outpath_withf).parent.mkdir(parents=True, exist_ok=True,mode=0o777)  #Maybe change mode?
        
        shutil.copyfile(filename, outpath_withf)


def main():
    if (len(sys.argv) == 2): 
        in_path = sys.argv[1]
    else:
        #Raw strings if you're on windows!
        in_path = REPO_CSV_PATH

    clone_verilog_repos(in_path)


#Executes main automatically
if __name__ == "__main__":
    main()