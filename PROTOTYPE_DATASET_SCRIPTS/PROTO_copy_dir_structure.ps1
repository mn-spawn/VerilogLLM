#NOTE: This script copies a file directory structure into a new path
#   I use relative paths for my Verilog folders here, but you can use w/e

$source='..\unstructured_verilog_files\'
$dest='..\synth_unstructured_verilog_files\'

robocopy $source $dest /e /xf *.*

$source='..\structured_verilog_files\'
$dest='..\synth_structured_verilog_files\'

robocopy $source $dest /e /xf *.*