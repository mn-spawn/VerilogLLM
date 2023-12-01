:: Author: Daniel Mendes
:: Date: 11/30/23
:: Class: CS 46x - Capstone Project
:: Group: Child AI (Tentative Name)
:: Description:
::  This is a .bat file that loads a Verilog file into Yosys, synthesizes it w/the 
::  provided general-purpose "synth" command, and then writes it to a new file. 
::  
::  Later versions of this script should synthesize it at different/lower levels, 
::  depending on the goals and our actual progress we made on the project. 
:: Version: 0.2.0 

@echo off

rem Nota Bene: This script MUST be run in the OSS-CAD Suite


::
:: SPECIFY THE SOURCE/DESTINATION DIRECTORIES CONTAINING THE VERILOG FILES
:: DO NOT INCLUDE THE FINAL "\"
::

set src="TYPE PATH HERE"

set dst="TYPE PATH HERE"


::
:: DO NOT TOUCH ANYTHING BELOW
::

set src2=%src:"=%
set dst2=%dst:"=%

rem -S = shortcut for 'synth', -o = outfile, '-f verilog' parses this as verilog

rem Some useful debugging prints
rem for /R %src% %%f in (*.v) do echo "%%f"
rem for /R %src% %%f in (*.v) do echo "%%~nf.v"
rem for /R %src% %%f in (*.v) do echo "%dst2%\synth_%%~nf.v"

for /R %src% %%f in (*.v) do yosys -o "%dst2%\synth_%%~nf.v" -S -f verilog "%%f"