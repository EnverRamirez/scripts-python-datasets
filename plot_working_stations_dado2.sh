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
number_of_stations=$(sort -k2,2nr different_Stations.txt | head -n1 | awk '{print $2}') #sorting by column in numerically reverse (descending) order

echo $year_with_more_stations $number_of_stations

#Get the station list of the year with more stations
station_list=$(cut -d';' -f2 ../dados2/${year_with_more_stations}_2.txt | uniq | grep -v Estacao)

#now plot the data using also python3
for station in ${station_list[@]}
do
for x in $(seq $start_year $end_year);do more ../dados2/${x}_2.txt |grep $station; done > tmp.txt 

###########################################
cat > plot_routine.py <<EOF
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

#open data file
fname='tmp.txt'

#read information of the data file
line_count = 0
with open(fname,'r') as file:
    for line in file:
        line_count += 1

#define precipitation, relative humidity and time
prec = np.empty([line_count], dtype = float)
ur = np.empty([line_count], dtype = float)
timestamp = np.empty([line_count], dtype = float)


#open data file to ingest information
f=open(fname, 'r')

#ingest info
idx=0
for line in f:
     line = line.strip()
     cols = line.split(';')
     prec[idx]=float(cols[6])
     ur[idx]=float(cols[5])
     date_str=str(cols[4].strip())
     dt=datetime.strptime(date_str, "%Y-%m-%d")
     year = dt.year
     day_of_year = dt.timetuple().tm_yday  # Day of year (1-366)
     frac_of_year = day_of_year / (366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365)
     timestamp[idx] = year + frac_of_year
     idx += 1

#indicate NaNs
prec[prec == -9999.0] = np.nan
ur[ur == -9999.0] = np.nan

#plot the data (use EC_indexes scripts as references)
fig,(ax,ax2)=plt.subplots(2)

ax.plot(timestamp, ur, color="black")
ax.set_title('Umidade Relativa (%)')
ax.spines['bottom'].set_visible(True)

ax2.plot(timestamp, prec, color="blue")
ax2.set_title('Precipitação (mm/day)')
ax.label_outer()

#plt.plot(timestamp, ur)
station=cols[0].strip()+" ("+cols[1].strip()+" Lat: "+cols[2].strip()+" Lon: "+cols[3].strip()+")"
fig.suptitle(station,fontsize=13)
#plt.tight_layout()
#plt.show()
plt.savefig("../plot_dados2/${station}.png")
plt.close()
EOF
###########################################

python3 plot_routine.py


#echo $station
done
