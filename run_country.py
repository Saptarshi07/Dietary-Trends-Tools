import matplotlib.pyplot as plt
from dietary_faotools import *
import csv


#An example of how the get_land_saved(area_code, group, calorie_level,year) function works:

#get_land_saved(231, 'meats', 2000, 2002)  


#the following is an outlier removal control (outlier removed using interquartile range method). If you wish to remove outliers from result set it to 'yes' or let it remain at default 'no'. If it is set to anything else, it will give the default result.

outlier_removal = 'yes'

#the following piece of code generates the plot of land-spared (total,remote and local) vs years (from start_year to end_year, which are currently, as of July 2019, 1961 and 2013 respectively) for a particular food-group ( any one from 'fruits', 'vegetables','oils', 'sugar','meats', 'dairy') for a particular country.

#set the variable region to the country_code of the country for which you want to observe land-spared vs years. You will find a mapping of country name to country code in CountryGroupFBS.csv

region = 231 #set to the country_code of the United States of America
group = 'sugar'#any one from 'fruits', 'vegetables','oils', 'sugar', 'meats' or 'dairy'
start_year = 1961 #the first year for which data is available in FAO as of July 2019
end_year = 2013 #the latest year for which data is available in FAO as of July 2019
land_use_dict = {}

for year in range(start_year,end_year + 1):
    result = get_land_saved(region, group, 2000, year) #calorie-level is set to 2000 kcal/person/day. You may only change it to 1000 kcal/person/day    
    local_res = result['local']
    remote_res = result['remote']
    total_res = result['total']
    #printing year just for clocking the code
    print(year)
    land_use_dict[year] = (total_res,local_res,remote_res)
    
if outlier_removal == 'yes':
    new_land_dict = remove_outlier(land_use_dict,0)
    new_land_dict = remove_outlier(new_land_dict,2)
    land_use_dict = new_land_dict
    
plt.plot(land_use_dict.keys(),[x[2] for x in list(land_use_dict.values())],'-o',label = 'total') #plots the total land-spared vs years
plt.plot(land_use_dict.keys(),[x[0] for x in list(land_use_dict.values())],'-o', label = 'local') #plots the local land-spared vs years
plt.title("%s" %group + ", " + areapd.loc[areapd['Country Code'] == region]['Country'].values[0])
plt.legend()
plt.show()

#the following part writes the results of land-spared vs years into result.csv. Every time youu run a new csv will be created
csvData = [['year', 'total(ha)', 'local(ha)', 'remote(ha)']]
for _item in land_use_dict.keys():
    csvData.append([_item,land_use_dict[_item][0], land_use_dict[_item][1], land_use_dict[_item][2]])
    
with open('result.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()
