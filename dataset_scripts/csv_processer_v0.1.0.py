############################################################################################
# Author: Daniel Mendes
# Date: 2/25/2024
# Class: CS 46x - Capstone Project
# Group: Child AI (Tentative Name)
# Description:
#   This file is used to remove comments and other junk from our gathered dataset of 
#   Verilog files. This time explicitly with a CSV parser and regex. 
#   This is an altered version that (hopefully) maintians metadata.  
#   This still needs to remove more junk.
############################################################################################

import csv
import sys
import re

maxInt = sys.maxsize
maxInt = int(maxInt)
csv.field_size_limit(1000000000) # sys max doesn't work


in_paths = [r"ALL FILE PATHS"
            ]
out_paths = [r"ALL FILE PATHS"
            ]

#Automatic single-line excludes
excludeArr = [
    "//",
    "Open Scope",
    "Require Import",
    "include"
]
for i in range(len(in_paths)):
    with open(in_paths[i], encoding='utf-8') as inf:
            #DictReader is used to grab specific rows
            #   Documentation: https://courses.cs.washington.edu/courses/cse140/13wi/csv-parsing.html
            reader = csv.DictReader(inf)


            with open(out_paths[i], "w", encoding='utf-8') as outf:
                writer = csv.DictWriter(outf, ["repo_name","path","copies","size","content","license"])
                writer.writeheader()
                for row in reader:
                    #https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
                    #TO REMOVE:
                    #   Misc. COQ Code
                    string = row["content"]
                    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
                    string = re.sub(re.compile("(\*.*?\*)",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
                    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string

                    string = re.sub(r'.{500,}\n?', '', string)

                    string = re.sub(re.compile("Section lemmas*.*?End lemmas",re.DOTALL ) ,"" ,string) # Remove all "lemmas" sections
                    #string = re.sub(re.compile("Proof.*.*?Qed.",re.DOTALL ) ,"" ,string) # BROKEN
                    #string = re.sub(re.compile("Proof.*.*?Abort.",re.DOTALL ) ,"" ,string) # BROKEN

                    string = re.sub(re.compile("`pragma protect data_block*.*?end_protected",re.DOTALL ) ,"" ,string) # Removes giant protected data blocks
                    string = re.sub(re.compile("`pragma protect key_block*.*?=",re.DOTALL ) ,"" ,string) # Removes key blocks? Not 100% accurate though, since some keys don't end with "="
                    string = re.sub(re.compile("`pragma.*?\n",re.DOTALL ) ,"" ,string) # Removes all single line pragma bloks

                    string = re.sub(re.compile("Open Scope.*?\n" ) ,"" ,string) # Removes single-line exclude
                    string = re.sub(re.compile("Require Import.*?\n" ) ,"" ,string) # Removes single-line exclude
                    string = re.sub(re.compile("include.*?\n" ) ,"" ,string) # Removes single-line exclude
                    row["content"] = string
                    writer.writerow(row)
            outf.close
            

                
                
            
            inf.close() 