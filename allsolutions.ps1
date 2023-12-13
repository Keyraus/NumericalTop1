#for each solution file in the current directory
#suppr every file in the output directory
Remove-Item .\Output\* -Force



#from 1 to 10
for ($i=1; $i -le 10; $i++) {
    #run the program with the instance and the solution file
    python3 main.py .\Instances\small\instance$i.txt .\Solutions\solution$i.txt | Out-File -FilePath .\Output\output$i.txt
}

#do the mean of the line Gap of the output files
#get the line Gap of the output files and extract the number after the string "Gap : "
#do the mean of the line Gap of the output files
Get-Content .\Output\output*.txt | Select-String -Pattern "Gap : " | % { $_.ToString().Split(":")[1] } | Measure-Object -Average | Select-Object -ExpandProperty Average
Get-Content .\Output\output*.txt | Select-String -Pattern "Gap1 : " | % { $_.ToString().Split(":")[1] } | Measure-Object -Average | Select-Object -ExpandProperty Average