#!/bin/bash

# Check for arguments
if [ $# -eq 0 ]
  then
    echo "Usage : ${0} [Rep1] <Rep2> ..."
    exit 1
fi

# Declare empty list for files name
fList=() # List of files to proceed
outList=() # List of solutions files to creates
logList=() # List of logs files

# Iterate threw all repertory supplied
for dir in "$@"
do
    # Check and create repertory if it does not exist
    mkdir -p "$dir"/solutions

    # Iterates threw all files in the repertory
    for file in "$dir"/*.lp
    do
        fList+=(${file})
        outList+=("$dir/solutions/$(basename $file .lp).out")
        logList+=("$dir/solutions/$(basename $file .lp).glplog")
    done
done

# Run the solver in parallel using all vCPU (use -j to set a maximum count of vCPU)
# This command is more optimized if there is more process than core on the machine
parallel glpsol --lp {1} -o {2} --log {3} > /dev/null ::: "${fList[@]}" :::+ "${outList[@]}" :::+ "${logList[@]}"

