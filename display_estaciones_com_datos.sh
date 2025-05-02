: "

"

# Display plots that have more data
             #awk -F';' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); gsub(/^[ \t]+|[ \t]+$/, "", $3); if ($2 != "" && $3 != "") print $2"/" $3".png"}' *.BKP
for x in $(
             awk -F';' '{
                gsub(/^[ \t]+|[ \t]+$/, "", $2);        
                gsub(/^[ \t]+|[ \t]+$/, "", $3); 
                if ($2 != "" && $3 != "") print $2"/" $3".png"
                }' estaciones_com_datos.txt.BKP )
do display $x
done

#gsub(/^[ \t]+|[ \t]+$/, "", $1) - Trims whitespace from first column
#gsub(/^[ \t]+|[ \t]+$/, "", $2) - Trims whitespace from second column
#if ($1 != "" && $2 != "") - Only proceeds if both columns have data

