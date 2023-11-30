rem Nota Bene: Must be run in the OSS-CAD Suite
rem ONLY EDIT THE PATHS FOR 'src' AND 'dst'

@echo off
set src="insert path here"
set src2=%src:"=%


set dst="insert path here"
set dst2=%dst:"=%


rem -S = shortcut for 'synth', -o = outfile, '-f verilog' parses this as verilog

rem Some useful debugging prints
rem for /R %src% %%f in (*.v) do echo "%%f"
rem for /R %src% %%f in (*.v) do echo "%%~nf.v"
rem for /R %src% %%f in (*.v) do echo "%dst2%\synth_%%~nf.v"

for /R %src% %%f in (*.v) do yosys -o "%dst2%\synth_%%~nf.v" -S -f verilog "%%f"