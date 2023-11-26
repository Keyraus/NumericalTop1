# For each file in ./Instances/small-lp, run the glpsol solver
fList=()
outList=()
logList=()
for dir in "$@"
do
    mkdir "$dir"/solutions
    for file in "$dir"/*.lp
    do
        fList+=(file)
        #echo "Running glpsol on $file"
        # Create an output file based on the input file name and stored in ./Instances/small-lp/solutions
        outList+=("./Instances/small-lp/solutions/$(basename $file .lp).out")
        logList+=("./Instances/small-lp/solutions/$(basename $file .lp).glplog")
        # Run glpsol on the input file and store the output in the output file
        #glpsol --lp $file -o $output_file.out --log $log_file.glplog > /dev/null &

        
    done
done
parallel glpsol --lp {1} -o {2} --log {3} > /dev/null ::: "${fList[@]}" :::+ "${outList[@]}" :::+ "${logList[@]}"
wait
