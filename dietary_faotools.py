import pandas as pd
import math
import numpy as np
from constants import *

#reads all the csvs in the drive as pandas dataframes
foodbalancepd = pd.read_csv('FoodBalanceSheets_E_All_Data_NOFLAG.csv',encoding = "ISO-8859-1")
fbn = foodbalancepd.loc[foodbalancepd['Item Code'].isin(items_under_consideration)]
areapd = pd.read_csv('CountryGroupFBS.csv', encoding = "ISO-8859-1")
cropspd = pd.read_csv('Production_Crops_E_All_Data.csv', encoding = "ISO-8859-1")
livestockpd = pd.read_csv('Production_LivestockPrimary_E_All_Data.csv',encoding = "ISO-8859-1")
tradelive = pd.read_csv('Trade_LiveAnimals_E_All_Data.csv',encoding = "ISO-8859-1")
livestockprocessed = pd.read_csv('Production_LivestockProcessed_E_All_Data.csv',encoding = "ISO-8859-1")
tradepd = pd.read_csv('Trade_Crops_Livestock_E_All_Data.csv',encoding = "ISO-8859-1")
landusepd = pd.read_csv('Inputs_LandUse_E_All_Data_NOFLAG.csv',encoding = "ISO-8859-1") 
table9pd = pd.read_csv('table9.csv')
liveanimalspd = pd.read_csv('Production_Livestock_E_All_Data.csv',encoding = "ISO-8859-1")
table2pd = pd.read_csv('table2.csv')
table7pd = pd.read_csv('table7.csv')
table6pd = pd.read_csv('table6.csv')
table4pd = pd.read_csv('table4.csv')
table10pd = pd.read_csv('table10.csv')

def get_masses_per_group(area_code, group, calorie_level, year):
#returns the masses of food per group required by an entire area in a year. The calorie distribution of either 2000kcal/day or 1000kcal/day by USDA 2010 are used here.
    
    pop = get_estimated_data_for(foodbalancepd,area_code,2501,511,year)*1000
    calorie_breakdown = calorie_intakes[calorie_level][group]
    dictionary = {}
    calorie_parts = {}
    calorie_distribution = {}
    mass_per_sub_group = {}
    for sub_group in food_groups[group]: 
        val = get_estimated_data(fbn,area_code,sub_group,664,year)
        #val = get_fbndata_for(area_code,sub_group,664,year)
        #val = fbn.loc[(fbn['Element Code'] == 664) & (fbn['Area Code'] == area_code) & (fbn['Item Code'] == sub_group)]['Y' + str(year)]

        dictionary[sub_group] = val

    for sub_group in food_groups[group]:
        calorie_parts[sub_group] = dictionary[sub_group]/(sum(dictionary.values())) if sum(dictionary.values())!= 0.0 else 0.0
        calorie_distribution[sub_group] = calorie_parts[sub_group]*calorie_breakdown
        
    for sub_group in food_groups[group]:
        food = get_estimated_data(fbn,area_code,sub_group,food_code,year)*1000
        val_cal = get_estimated_data(fbn,area_code,sub_group,664,year)
        if calorie_distribution[sub_group] != 0:
            value = food/(val_cal*365*pop) 
        else:
            value = 0.0
        value = value*calorie_distribution[sub_group]
        mass_per_sub_group[sub_group] = value*365*pop
    return mass_per_sub_group
 


def get_land_saved(area_code, group, calorie_level, year):
    
    #gives land spared if the population of the area adheres to USDA guidelines of x calorie level (either 1000 or 2000) at a particular year. 'group' argument determines land-saved due to consumption of that particular group. can either be 'fruits', 'vegetables', 'meats', 'dairy', 'grains', 'oils', 'sugar'.
    
    res_land_saved = 0
    res_land_saved_imports = 0
    res_land_saved_domestic = 0
    for sub_group in food_groups[group]:
        
        food = get_estimated_data(fbn,area_code,sub_group,food_code,year)*1000
        domestic = get_estimated_data(fbn,area_code,sub_group,domestic_code,year)*1000
        imports = get_estimated_data(fbn,area_code,sub_group,imports_code,year)*1000
        if domestic!= 0.0:
            idr = imports/domestic 
        else:
            idr = 1.0
        
        
        yld = get_weighted_yield(area_code,sub_group,year)
        world_yld = get_weighted_yield(world_code,sub_group,year)
        
        
            
        imports_adj = (idr*food)/b2p_conversions[sub_group]
        food_adj = (food - imports_adj)/b2p_conversions[sub_group]
        
        if yld == 0.0:
            idr = 1.0
            imports_adj += food_adj
            food_adj = 0.0
            yld = 1.0
        
        
        land_local = food_adj/yld
        land_remote = imports_adj/world_yld
        land_total = land_local + land_remote
        
        rec_import = idr*get_masses_per_group(area_code, group, calorie_level, year)[sub_group]
        rec_food =  get_masses_per_group(area_code, group, calorie_level, year)[sub_group] - rec_import
        
        rec_land_local = rec_food/yld
        rec_land_remote = rec_import/world_yld
        rec_land_total = rec_land_local + rec_land_remote
        
        diff_land_local = land_local-rec_land_local
        diff_land_remote = land_remote - rec_land_remote
        diff_land_total = land_total - rec_land_total
        
        res_land_saved += diff_land_total
        res_land_saved_imports += diff_land_remote
        res_land_saved_domestic += diff_land_local
    return {'local': res_land_saved_domestic, 'remote': res_land_saved_imports, 'total': res_land_saved }
        
  
def get_weighted_cropyield(area_code,item_code,year):
    
    #returns yield of an item_code under crops (and not livestock) in tonnes/ha
    
    production = 0.0
    area_harvested = 0.0
    _list_of_products = b2p_mappings[item_code]
    for item in _list_of_products:
        p = get_estimated_data(cropspd,area_code,item,production_code,year)
        a = get_estimated_data(cropspd,area_code,item,area_harvested_element_code,year)
        production += p
        area_harvested += a
    wyield = production/area_harvested if area_harvested != 0 else 0.0
    return wyield
        


def get_weighted_yield(area_code,item_code,year):
    
    #returns yield of any item_code (under consideration in Rizhvi et al.) in tonnes/ha 
    
    production = 0.0
    area_harvested = 0.0
    _list_of_products = b2p_mappings[item_code]
    production = 0
    area_harvested = 0
    for item in _list_of_products:
        if item in livestock_product_codes:
            p = get_livestock_production(area_code,all_codes_similar_mappings[item],year)['T']
            a = get_livestock_area_harvested(area_code,item,year)
        else:
            p = get_estimated_data(cropspd,area_code,item,production_code,year)
            a = get_estimated_data(cropspd,area_code,item,area_harvested_element_code,year)
        production += p
        area_harvested += a
    wyield = production/area_harvested if area_harvested != 0 else 0.0
    return wyield
            


def get_estimated_data(df,area_code,item_code,element_code,year):
    
    #reads off the dataframe df the data for an 'area-code', 'item_code', 'element_code', 'year' tuple. If no data is available it looks for data in the next and previous year data. If no data is avaiilable, returns 0.0
    
    data = df.loc[(df['Area Code'] == area_code) & (df['Item Code'] == item_code) & (df['Element Code'] == element_code)]
    next_prev = get_next_prev_year(year)
    if data['Y' + str(year)].empty:
        for j in next_prev:
            if data['Y' + str(j)].empty != 1:
                if data['Y' + str(j)].isnull().values[0] != 1:
                    return j
        return 0.0
        
    elif data['Y' + str(year)].isnull().values[0]:
        for j in next_prev:
            if data['Y' + str(j)].empty != 1:
                if data['Y' + str(j)].isnull().values[0] != 1:
                    return j
        return 0.0
    else:
        return data['Y' + str(year)].values[0]
    
def get_estimated_data_for(df,area_code,item_code,element_code,year):
    
    #reads off the dataframe df the data for an 'area-code', 'item_code', 'element_code', 'year' tuple. If no data is available it looks for data in the next and previous year data. If no data is available in those years it looks for data in the continent in which that area falls (or if area_code is a continent it looks for world average data).  
    
    if area_code not in region_codes.keys() and area_code not in continent_codes.keys():
        _val = get_estimated_data(df,area_code,item_code,element_code,year)
        if math.isnan(_val) or _val == 0:
            continent_code = list(set(areapd.loc[areapd['Country Code'] == area_code]['Country Group Code'].tolist()).intersection(set(list(continent_codes.keys()))))[0]
            _val_continent = get_estimated_data(df,continent_code,item_code,element_code,year)
            if math.isnan(_val_continent):
                return get_estimated_data(df,world_code,item_code,element_code,year)
            else:
                return _val_continent
        else:
            return _val
    else:
        _val = get_estimated_data(df,area_code,item_code,element_code,year)
        if math.isnan(_val) or _val ==0:
            return get_estimated_data(df,world_code,item_code,element_code,year)
        else:
            return _val

def get_next_prev_year(year):
    if year == start_year:
        return [start_year + 1]
    elif year == end_year:
        return [end_year - 1]
    else:
        return [year-1,year+1]
    
def get_sub_continent(area_code):
    
    #a function to find out the sub-continent of an area_code
    
    _area_subcontinent = list(set(areapd.loc[areapd['Country Code'] == area_code]['Country Group Code'].tolist()).intersection(subcontinent_codes))[0]
    if _area_subcontinent == 5302:
        _area_subcontinent = 5300
    elif _area_subcontinent == 5304:
        _area_subcontinent = 5303
    elif _area_subcontinent == 5504:
        _area_subcontinent = 5500
    elif _area_subcontinent == 5706:
        _area_subcontinent = 5400
    return _area_subcontinent



def get_livestock_production(area_code,item_code,year,_import = True, _export = True, _cull = True):

#returns adjusted livestock production of the livestock item-code. Adjustment done as per the supplementary of Rizhvi et al.
    
    
    if item_code == 1058:
        _item_code = 1808
    else:
        _item_code = item_code
    #done
    if _item_code != butter_code:
        _production = get_estimated_data(livestockpd,area_code,_item_code,production_code,year) #this is in tonnes
    else:
        _production = get_estimated_data(livestockprocessed,area_code,_item_code,production_code,year)#in tonnes
    _import = get_estimated_data(tradepd,area_code,_item_code,import_quantity_code,year) #in tonnes
    _export = get_estimated_data(tradepd,area_code,_item_code,export_quantity_code,year) #in tonnes
    net_production = _production + _export - _import
    #in tonnes
    _prod = {'T':net_production, 'P':0.0,'ML':0.0}
    
    if area_code != world_code:
        _area_subcontinent = get_sub_continent(area_code) 
    else:
        _area_subcontinent = world_code
        
    _dict_ML =  table2pd.loc[(table2pd['aggregatecode'] == _area_subcontinent) & (table2pd['system'] == 'ML') & (table2pd['itemcode'] ==_item_code)].to_dict()
    a_ml, b_ml, c_ml = list(_dict_ML['a'].values())[0],list(_dict_ML['b'].values())[0],list(_dict_ML['c'].values())[0]
    year_p = year - 1970
    ml_frac = a_ml*(year_p**2) + b_ml*(year_p) + c_ml
    if ml_frac > 1:
        ml_frac = 1
    elif ml_frac < 0:
        ml_frac = 0
    else:
        ml_frac = ml_frac
    p_frac = 1 - ml_frac
    _prod['P'] = net_production*p_frac
    _prod['ML'] = net_production*ml_frac
    #returns in tonnes
    return _prod
    

    
    
def get_the_ML_frac(table,sub_continent,item_code,year):
    #reads of the ML frac part from Bowman tables: table2,4,6,7,9.
    
    year_p = year - 1970
    _dict_ML =  table.loc[(table['aggregatecode'] == sub_continent) & (table['system'] == 'ML') & (table['itemcode'] == item_code)].to_dict()
    a_ml, b_ml, c_ml = list(_dict_ML['a'].values())[0],list(_dict_ML['b'].values())[0],list(_dict_ML['c'].values())[0]
    _val = a_ml*(year_p**2) + b_ml*(year_p) + c_ml
    if _val < 0:
        return 0
    elif _val >1:
        return 1
    else:
        return _val
    
    
    
    
    
def get_the_P_frac(table,sub_continent,item_code,year):
    #reads of the P frac part from Bowman tables: table2,4,6,7,9.
    year_p = year - 1970
    _dict_ML =  table.loc[(table['aggregatecode'] == sub_continent) & (table['system'] == 'P') & (table['itemcode'] == item_code)].to_dict()
    a_ml, b_ml, c_ml = list(_dict_ML['a'].values())[0],list(_dict_ML['b'].values())[0],list(_dict_ML['c'].values())[0]
    _val = a_ml*(year_p**2) + b_ml*(year_p) + c_ml
    if _val < 0:
        return 0
    elif _val >1:
        return 1
    else:
        return _val
    
    
def get_the_ML_val(table,sub_continent,item_code,year):
    #reads of the ML value from Bowman tables: table10.
    year_p = year - 1970
    _dict_ML =  table.loc[(table['aggregatecode'] == sub_continent) & (table['system'] == 'ML') & (table['itemcode'] == item_code)].to_dict()
    a_ml, b_ml, c_ml = list(_dict_ML['a'].values())[0],list(_dict_ML['b'].values())[0],list(_dict_ML['c'].values())[0]
    _val = a_ml*(year_p**2) + b_ml*(year_p) + c_ml
    return _val

def get_the_P_val(table,sub_continent,item_code,year):
    #reads of the ML value from Bowman tables: table10.
    year_p = year - 1970
    _dict_ML =  table.loc[(table['aggregatecode'] == sub_continent) & (table['system'] == 'P') & (table['itemcode'] ==item_code)].to_dict()
    a_ml, b_ml, c_ml = list(_dict_ML['a'].values())[0],list(_dict_ML['b'].values())[0],list(_dict_ML['c'].values())[0]
    _val = a_ml*(year_p**2) + b_ml*(year_p) + c_ml
    return _val


    
        
    
    
    
def get_pastoral_mixed_landless(area_code,item_code,year):
    
    #returns the pasture area required for ruminant production (of a bovine/ovine meat product) in an area and a year. 'T' in the returned dictionary key indicates the total pasture area required to produce the bovine/ovine meat item code in the area_code. 'P' indicates the pastoral part of 'T' and 'ML' indicates the mixed landless part of it.
    
    if area_code != world_code:
        _area_subcontinent = get_sub_continent(area_code)
    else:
        _area_subcontinent = world_code
        
    total_pasture = get_estimated_data(landusepd,area_code,perm_pasture_code,area_element_code,year) + get_estimated_data(landusepd,area_code,temp_pasture_code,area_element_code,year)
    if total_pasture == 0.0:
        total_pasture = 0.69*get_estimated_data(landusepd,world_code,agriculture_land_code,area_element_code,year)
    #this gives total pasture in 1000 hectares
 
    year_p = year - 1970
    _dict_P = table9pd.loc[(table9pd['aggregatecode'] == _area_subcontinent) & (table9pd['system'] == 'P')].to_dict()
    _dict_ML = table9pd.loc[(table9pd['aggregatecode'] == _area_subcontinent) & (table9pd['system'] == 'ML')].to_dict()
    
    #a_p, b_p, c_p = list(_dict_P['a'].values())[0],list(_dict_P['b'].values())[0],list(_dict_P['c'].values())[0]
    a_ml, b_ml, c_ml = list(_dict_ML['a'].values())[0],list(_dict_ML['b'].values())[0],list(_dict_ML['c'].values())[0]
    
    #p_frac = a_p*(year_p**2) + b_p*(year_p) + c_p
    ml_frac = a_ml*(year_p**2) + b_ml*(year_p) + c_ml
    if ml_frac < 0:
        ml_frac = 0
        p_frac = 1
    elif ml_frac > 1:
        ml_frac = 1
        p_frac = 0
    p_frac = 1 - ml_frac
        
    pastoral_area = total_pasture*p_frac #in 1000 hectares
    mixedlandless_area = total_pasture*ml_frac #in 1000 hectares
    
    stocks = {k:0.0 for k in bovine_meat_codes + ovine_meat_codes}
    
    for k in stocks.keys():
        _animal_code = meat_animal_mappings[k]
        mult = 1000 if liveanimalspd.loc[liveanimalspd['Item Code'] == _animal_code]['Unit'].values[0] == '1000 Head' else 1.0
        if k not in milkeggs_meat_mappings.values(): #an animal that does not produce milk/eggs
            stocks[k] = mult*get_estimated_data(liveanimalspd,area_code,_animal_code,stocks_code,year) #in heads
        else:
            _milkeggs_code = meat_milkeggs_mappings[k]
            stocks[k] = mult*get_estimated_data(liveanimalspd,area_code,_animal_code,stocks_code,year) - get_estimated_data(livestockpd,area_code,_milkeggs_code,producing_animals_code,year)
    
    new_stocks = {k:0.0 for k in bovine_meat_codes + ovine_meat_codes}
    for k in stocks.keys():
        similar_animal_meat = table267_similar_codes[k]
        _prod = get_estimated_data_for(livestockpd,area_code,k,production_code,year)
        _carcass = get_estimated_data_for(livestockpd,area_code,k,carcass_weight_code,year)*0.0001
        _offtake = get_estimated_data_for(livestockpd,area_code,k,producing_animals_code,year)
        
        _prod_ml = get_the_ML_frac(table2pd,_area_subcontinent,similar_animal_meat,year)*_prod
        _carcass_ml = get_the_ML_frac(table6pd,_area_subcontinent,similar_animal_meat,year)*_carcass
        _offtake_ml = get_the_ML_frac(table7pd,_area_subcontinent,similar_animal_meat,year)*_offtake
        
        _prod_p = _prod - _prod_ml
        _carcass_p = _carcass - _carcass_ml
        _offtake_p = _offtake - _offtake_ml
        
        ratio_p = (_prod_p*_offtake_p)/_carcass_p if _carcass_p != 0 else 0.0
        ratio_ml = (_prod_ml*_offtake_ml)/_carcass_ml if _carcass_ml != 0 else 0.0
        
        _p_ratio = ratio_p/(ratio_p + ratio_ml) if ratio_p + ratio_ml !=0 else 0.0
        _ml_ratio = ratio_ml/(ratio_p + ratio_ml) if ratio_p + ratio_ml !=0 else 0.0
        
        stocks_P = stocks[k]*_p_ratio
        new_stocks[k] = {'P': stocks_P, 'ML': stocks[k] - stocks_P}
    
    _val_P = new_stocks[item_code]['P']
    _val_ML = new_stocks[item_code]['ML']
    _set_P = [new_stocks[k]['P'] for k in new_stocks.keys()]
    _set_ML = [new_stocks[k]['ML'] for k in new_stocks.keys()]
    
    _value_P = _val_P*pastoral_area/sum(_set_P) if sum(_set_P) != 0 else 0.0
    _value_ML = _val_ML*mixedlandless_area/sum(_set_ML) if sum(_set_ML) != 0 else 0.0
    
    #this returns in hectares
    return {'T':_value_P*1000 + _value_ML*1000,'P':  _value_P*1000, 'ML': _value_ML*1000}
    
    
    
def get_cropland_feed_area(area_code,item_code,year):
    #returns the cropland area used for feed of the source animal that generates the livestock product item_code. Returns in hectares of land.
    
    year_p = year - 1970
    if area_code != world_code:
        _area_subcontinent = get_sub_continent(area_code)
    else:
        _area_subcontinent = world_code
        
    _frac_dict = {k: 0.0 for k in all_codes + [886]}
    
    for k in _frac_dict.keys():
        
        _prod = get_livestock_production(area_code,all_codes_similar_mappings[k],year)
        
        
        _item_type = table4_code_reverse_mappings[all_codes_similar_mappings[k]] 
        _dict_r =  table4pd.loc[(table4pd['aggregatecode'] == _area_subcontinent) & (table4pd['itemtypecode'] == _item_type)].to_dict()
        a_r, b_r, c_r = list(_dict_r['a'].values())[0],list(_dict_r['b'].values())[0],list(_dict_r['c'].values())[0]
        r_frac = a_r*(year_p**2) + b_r*(year_p) + c_r
        if r_frac >1:
            r_frac = 1
        elif r_frac <0:
            r_frac = 0
        
        
        _similar_item = all_codes_similar_mappings[k]
        if _similar_item == 1035 or _similar_item == 1058:
            f_k = get_the_ML_val(table10pd,_area_subcontinent,table10_reverse_mappings[_similar_item],year)
        else:
            f_k = get_the_P_val(table10pd,_area_subcontinent,table10_reverse_mappings[_similar_item],year) + get_the_ML_val(table10pd,_area_subcontinent,table10_reverse_mappings[_similar_item],year)
        _frac_dict[k] = _prod['ML']*r_frac*(f_k)
        #print(_frac_dict[k],r_frac)
    feed_share = _frac_dict[item_code]/sum(_frac_dict.values()) if sum(_frac_dict.values()) != 0 else 0.0
    #print(feed_share)
    
    _sum = 0
    
    for feed_element in feed_items_in_crops:
        ssr = get_ssr(area_code,feed_element,year)
        if ssr > 1 or ssr < 0:
            ssr = 1.0
        feed_amount = get_estimated_data(foodbalancepd,area_code,crops_to_balance_mapping[feed_element],feed_code,year)
        
        feed_quantity = feed_share*ssr*feed_amount*1000 #in tonnes now
        
        _yield = get_estimated_data(cropspd,area_code,feed_element,yield_code,year)
        feed_quantity = feed_quantity/(0.0001*_yield) if _yield != 0 else 0.0
        _sum += feed_quantity
        #print(feed_quantity)
        
    #returns in hectares
    return _sum
    
def get_ssr(area_code,item_code,year):
    #returns the self-sufficiency ratio of a country for a particular item_code. (defined in Supp. Rizhvi et al.)
    
    #here the item_code is item_code in food_balance_sheet
    _prod = get_estimated_data(cropspd,area_code,item_code,production_code,year)
    _imp =  get_estimated_data(tradepd,area_code,item_code,import_quantity_code,year)
    _exp =  get_estimated_data(tradepd,area_code,item_code,export_quantity_code,year)
    return _prod/(_prod + _imp - _exp) if (_prod + _imp - _exp)!= 0 else 0.0

def get_livestock_offtake(area_code,item_code,year):

#returns in Head (Supp. Rizhvi et al.)
    _num_prod_animals = get_estimated_data(livestockpd,area_code,item_code,producing_animals_code,year)  
    _off = {'T': _num_prod_animals, 'P':0.0,'ML':0.0}
    _area_subcontinent = get_sub_continent(area_code)    
    _dict_ML =  table7pd.loc[(table7pd['aggregatecode'] == _area_subcontinent) & (table7pd['system'] == 'P') & (table7pd['itemcode'] == item_code)].to_dict()
    a_ml, b_ml, c_ml = list(_dict_ML['a'].values())[0],list(_dict_ML['b'].values())[0],list(_dict_ML['c'].values())[0]
    year_p = year - 1970
    ml_frac = a_ml*(year_p**2) + b_ml*(year_p) + c_ml
    if ml_frac > 1:
        ml_frac = 1
    if ml_frac <0:
        ml_frac = 0
    p_frac = 1 - ml_frac
    _off['P'] = _num_prod_animals*p_frac
    _off['ML'] = _num_prod_animals*ml_frac
    return _off

def get_livestock_area_harvested(area_code,item_code,year):
    
    #returns in hectares the area required to produce a livestock item_code in an area_code
    _cropland_feed_area = get_cropland_feed_area(area_code,item_code,year)
    if item_code in bovine_meat_codes + ovine_meat_codes:
        _pasturemixedlandless = get_pastoral_mixed_landless(area_code,item_code,year)
        return _cropland_feed_area + _pasturemixedlandless['T']
    else:
        return _cropland_feed_area 
    #returns in hectares
        
        
def get_livestock_yield(area_code,item_code,year):
    
    #returns the yield in tonnes/ha of a livestock item_code
    if item_code in bovine_meat_codes + ovine_meat_codes:
        _prod = get_livestock_production(area_code,all_codes_similar_mappings[item_code],year)
        _cropland_feed_area = get_cropland_feed_area(area_code,item_code,year)
        _pasturemixedlandless = get_pastoral_mixed_landless(area_code,item_code,year)
        return (_prod['T'])/(_cropland_feed_area + _pasturemixedlandless['P'] + _pasturemixedlandless['ML']) if (_cropland_feed_area + _pasturemixedlandless['P'] + _pasturemixedlandless['ML'])!=0.0 else 0.0
    else:
        _prod = get_livestock_production(area_code,all_codes_similar_mappings[item_code],year)
        _cropland_feed_area = get_cropland_feed_area(area_code,item_code,year)                
        return _prod['T']/_cropland_feed_area if _cropland_feed_area != 0 else 0.0
#returns in tonnes/hectare
 
def remove_outlier(dictionary,field):
#returns a dictionary of land_spared vs year without the outlier points in the data of the field
# specified. Field can either be 'local', 'remote' or 'total'.
    if field == 'local':
        field = 0
    elif field == 'remote':
        field = 1
    elif field == 'total':
        field = 2
    q1 = np.percentile([x[field] for x in list(dictionary.values())],25)
    q3 = np.percentile([x[field] for x in list(dictionary.values())],75)
    iqr = abs(q1 - q3)
    val1 = q1 - 1.5*iqr
    val2 = q3 + 1.5*iqr
    new_dict = {}
    for i in dictionary.keys():
        if dictionary[i][field] < val2 and dictionary[i][field] > val1:
            new_dict[i] = dictionary[i]
    return new_dict    
