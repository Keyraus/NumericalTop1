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

# Iterate threw all repertory supplied
for dir in "$@"
do
    # Iterates threw all files in the repertory
    for file in "$dir"/*.txt
    do
        fList+=(${file})
        outList+=("$dir/$(basename $file .txt).lp")
    done
done

# Run the python code in parallel using all vCPU (use -j to set a maximum count of vCPU)
# This command is more optimized if there is more process than core on the machine
parallel python3 ./convertion.py {1} {2} ::: "${fList[@]}" :::+ "${outList[@]}"

