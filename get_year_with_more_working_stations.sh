: '
In this code we get station codes to identify which year has
more different stations
'
start_year=2014
end_year=2024

# Obtain the year with more working stations
for x in $(seq $start_year $end_year);
do
#list stations removing entry Estacao (the header in this case)
stations=$(cut -d';' -f2 ../dados2/${x}_2.txt | uniq | grep -v Estacao| wc -l) #get a unique name then count
echo $x $stations
done > different_Stations.txt

year_with_more_stations=$(sort -k2,2nr different_Stations.txt | head -n1 | awk '{print $1}')
number_of_stations=$(sort -k2,2nr different_Stations.txt | head -n1 | awk '{print $2}')

echo $year_with_more_stations $number_of_stations

cut -d';' -f2 ../dados2/${year_with_more_stations}_2.txt | uniq | grep -v Estacao > year_with_more_stations.txt
