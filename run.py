import matplotlib.pyplot as plt
from dietary_faotools import *


#An example of how the get_land_saved(area_code, group, calorie_level,year) function works:

#get_land_saved(231, 'meats', 2000, 2002)  


#the following piece of code generates the plot of land-spared (total,remote and local) vs years (from start_year to end_year, which are currently, as of July 2019, 1961 and 2013 respectively) for a particular food-group ( any one from 'fruits', 'vegetables','oils', 'sugar', 'meats', 'dairy') for a particular region (works for any region in dictionary values of region_codes. The sub-regions in the supplemantary of Rizhvi et al. are called here as 'Africa', 'Asia', 'Northern America', 'South America', 'Eastern Europe', 'European Union', 'Oceania')


#set the region for which you want to observe land-spared vs years
region = 'European Union' #any region from the values of the dictionary region_codes in constants.py. The region codes for generating results in supp of Rizhvi et al. were 'Africa', 'Asia', 'Northern America', 'South America', 'Eastern Europe', 'European Union', 'Oceania'. For viewing results for world use 'World'
group = 'sugar'#any one from 'fruits', 'vegetables','oils', 'sugar', 'meats' or 'dairy'
start_year = 1961 #the first year for which data is available in FAO as of July 2019
end_year = 2013 #the latest year for which data is available in FAO as of July 2019


#the following is an outlier removal control (outlier removed using interquartile range method). If you wish to remove outliers from result set it to 'yes' or let it remain at default 'no'. If it is set to anything else, it will give the default result.

outlier_removal = 'yes'


land_use_dict = {}
for year in range(start_year,end_year + 1):
    local_res = 0.0
    remote_res = 0.0
    total_res = 0.0
    for area in areapd.loc[areapd['Country Group'] == region]['Country Code'].tolist():
        result = get_land_saved(area, group, 2000, year)    
        local_res += result['local']
        remote_res += result['remote']
        total_res += result['total']
    land_use_dict[year] = (local_res,remote_res,total_res)
    #printing year just for clocking the code
    print(year)
    

    
if outlier_removal == 'yes':
    new_land_dict = remove_outlier(land_use_dict,0)
    new_land_dict = remove_outlier(new_land_dict,2)
    land_use_dict = new_land_dict
    
plt.plot(land_use_dict.keys(),[x[2] for x in list(land_use_dict.values())],'-o',label = 'total') #plots the total land-spared vs years
plt.plot(land_use_dict.keys(),[x[0] for x in list(land_use_dict.values())],'-o', label = 'local') #plots the local land-spared vs years
plt.title("%s" %group + ", " + region)
plt.legend()
plt.show()