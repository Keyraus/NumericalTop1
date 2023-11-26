# For each file in ./Instances/small-lp, run the glpsol solver
for file in ./Instances/small-lp/*.lp
do
    echo "Running glpsol on $file"
    # Create an output file based on the input file name and stored in ./Instances/small-lp/solutions
    output_file="./Instances/small-lp/solutions/$(basename $file .lp).out"
    log_file="./Instances/small-lp/solutions/$(basename $file .lp).glplog"
    # Run glpsol on the input file and store the output in the output file
    glpsol --lp $file -o $output_file --log $log_file &
done
wait
# 