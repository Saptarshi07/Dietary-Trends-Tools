items_under_consideration = [2919,2655,2918,2907,2905,2656,2658,2911,2912,2731,2732,2733,2734,2913,2949,2948,2740,2914,2908,2909,2922]

food_groups = {
'fruits':[2919,2655],
'vegetables':[2918,2907],
'grains':[2905,2656,2658],
'meats':[2911,2912,2731,2732,2733,2734,2913,2949],
'dairy':[2948, 2740],
'oils':[2914],
'sugar':[2908,2909,2922]
}

calorie_intakes = {
	1000 : {
		'fruits':93.12,
		'vegetables':34.18,
		'grains':266,
		'meats':108.67,
		'dairy':484.67,
		'oils':199,
		'sugar':165},
		
	2000 : {
		'fruits':186.24,
		'vegetables':87,
		'grains':532,
		'meats':298.84,
		'dairy':727,
		'oils':239,
		'sugar':267}
}


conversion_factor = {2655: 0.7, 2656: 4.78, 2658: 0.8, 2740: 0.047, 2914: 0.2, 2909: 0.12}

world_code = 5000

region_codes = {5000:"World",5101:"Eastern Africa",5102:"Middle Africa",5103:"Northern Africa",5104:"Southern Africa",5105:"Western Africa",5203:"Northern America",5204:"Central America",5206:"Carribbean",5207:"South America",5301:"Central Asia",5302:"Eastern Asia",5303:"Southern Asia",5304:"South-Eastern Asia",5305:"Western Asia",5401:"Eastern Europe",5402:"Northern Europe",5403:"Southern Europe",5404:"Western Europe",5501:"Australia and New Zealand",5502:"Melanesia",5503:"Micronesia",5504:"Polynesia",5100:"Africa",5200:"Americas",5300:"Asia",5400:"Europe",5500:"Oceania",5706:"European Union"}#,5600:"Antarctic Region"

continent_codes = {5100:"Africa",5200:"Americas",5300:"Asia",5400:"Europe",5500:"Oceania",}

subcontinent_codes = set(region_codes.keys()) - set(continent_codes.keys()) - set([world_code])






b2p_mappings = {
2656:[44], #beer
2658:[1717], #alcohol
2655:[560], #wine
2905:[1717], #cereal
#2919:[515,486,512,577,521,523,526,530,531,534,536,541,542,544,547,549,550,552,554,558,569,571,572,587,591,592,600,
#      603,619,507,560,497,490,574,489], #fruit
2919:[1738],    
2913:[1732], #oilcrops
2911:[1726], #pulses
2907:[1720], #roots
2909:[156,157,161], #sugar
2908:[156,157,161], #sugarcrops
2912:[1729], #treenuts
2918:[1735], #vegetables
2922:[661,656], #stimulants
2914:[1732], #oils
2731:[867], #beef
2732:[977,1017], #mutton
2733:[1035], #pork
2734:[1058], #poultry
2948:[882], #milk
2740:[886], #butter
2949:[1062], #eggs
}
b2p_conversions = {
2656:4.78, #beer
2658:0.6, #alcohol
2655:0.7, #wine
2905:1.0, #cereal
2919:1.0, #fruit
2913:1.0, #oilcrops
2911:1.0, #pulses
2907:1.0, #roots
2909:0.12, #sugar
2908:1.0, #sugarcrops
2912:1.0, #treenuts
2918:1.0, #vegetables
2922:1.0, #stimulants
2914:0.2, #oils
2731:1.0, #beef
2732:1.0, #mutton
2733:1.0, #pork
2734:1.0, #poultry
2948:1.0, #milk
2740:0.047, #butter
2949:1.0, #eggs
}


bovine_meat_codes = [867,947,1097,1108,1124,1127]#[867,947,977,1017,1097,1108,1124,1127]
bovine_codes = [866,946,1096,1107,1110,1126]
ovine_meat_codes = [977,1017]
ovine_codes = [976,1016]
milk_codes = [882,951,982,1020,1130]
pig_meat_codes = [1035]
pig_codes = [1034]
poultry_meat_codes = [1058,1069,1073,1080,1089]
poultry_codes = [1057,1068,1072,1079,1083]
egg_codes = [1062,1091]
all_codes = bovine_meat_codes+ovine_meat_codes+milk_codes+pig_meat_codes+poultry_meat_codes+egg_codes
meat_animal_mappings = {867:866,947:946,1097:1096,1108:1107,1124:1110,1127:1126,977:976,1017:1016,1035:1034,1058:1057,1069:1068,1073:1072,1080:1079,1089:1083}
meat_codes = meat_animal_mappings.keys()
animal_meat_mappings = {v:k for k,v in meat_animal_mappings.items()}
milkeggs_meat_mappings = {882:867,951:947,982:977,1020:1017,1062:1058,1130:1127,1091:1069}
meat_milkeggs_mappings = {867:882,947:951,977:982,1017:1020,1058:1062,1127:1130,1069:1091}
milkeggs_animal_mappings = {882:866,951:946,982:976,1020:1016,1062:1057,1130:1126,1091:1068}
milkeggsmeat_animal_mappings = {**milkeggs_animal_mappings,**meat_animal_mappings}
animal_milkeggs_mappings = {v:k for k,v in milkeggs_animal_mappings.items()}
producing_animals_group = 31
producing_animals_codes = [5320,5322,5318,5321,5313,5323,5319,5314]
khead_codes = [5321,5313,5323]
milking_codes = [5318]
laying_codes = [5313]
processed_codes = [5130]
items_that_use_pasture = bovine_meat_codes+ovine_meat_codes+milk_codes
butter_code = 886
milk_code = 882
table267_similar_codes = {867:867,947:867,1097:867,1108:867,1124:867,1127:867,977: 1807, 1017: 1807}
table4_code_mappings = {0:867,1:882,2:1807,3:1035,4:1058}
table4_code_reverse_mappings = {v:k for k,v in table4_code_mappings.items()}
table10_code_mappings = {'beef': 867, 'milk': 882, 'sheep & goats': 1807, 'pigs': 1035, 'poultry': 1058}
all_codes_similar_mappings = {867:867, 947:867, 1097:867, 1108: 867, 1124:867, 977: 1807, 1017: 1807, 
                             882: 882, 951: 882, 982: 1807, 1020: 1807, 1130: 882, 1035: 1035, 1058: 1058, 1069: 1058,
                             1073:1058, 1080:1058, 1089:1058, 1062:1058, 1091:1058, 1127: 867, 886:882}

table10_reverse_mappings = {v:k for k,v in table10_code_mappings.items()}



feed_categories = { #keys are food groups, first tuple entry is list of included itemcodes from commiditybalance, second tuple entry is list of corresponding itemcodes from productioncrops, third tuple entry (if present) is conversion factor to primary crop.
	"cereal":([2511,2804,2513,2514,2515,2516,2517,2518,2520],
			  [15,27,44,56,71,75,79,83,108],[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]),
	"roots":([2531,2532,2533,2534,2535],[116,125,122,149,137],[1.0,1.0,1.0,1.0,1.0]),
	"sugarcrops":([2536,2537],[156,157],[1.0,1.0]),
	"sugar":([2827],[156],[0.11]),
	"pulses":([2546,2547,2549],[176,187,191],[1.0,1.0,1.0]),
	"nuts":([2551],[1729],[1.0]),
	"oilcrops":([2555,2820,2557,2558,2559,2560,2561,2563,2570],[236,242,267,270,328,249,289,260,339],[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]),
	"oil":([2571,2572,2573,2574,2575,2576,2578,2579,2586],[236,242,267,270,328,254,249,289,339],[0.18,0.30,0.41,0.38,0.10,0.19,0.13,0.43,0.3]),
	"fruitnveg":([2601,2602,2605,2611,2612,2613,2614,2615,2616,2618,2619,2620,2625],[388,403,358,490,497,507,512,486,489,574,577,560,619],[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])}
feed_items_in_crops = feed_categories["cereal"][1]+feed_categories["roots"][1]+feed_categories["sugarcrops"][1]+feed_categories["sugar"][1]+feed_categories["pulses"][1]+feed_categories["nuts"][1]+feed_categories["oilcrops"][1]+feed_categories["oil"][1]+feed_categories["fruitnveg"][1]


livestock_product_codes = [867,977,1017,1035,1058,882,886,1062]

crops_to_balance_mapping = {15: 2511,
 27: 2804,
 44: 2513,
 56: 2514,
 71: 2515,
 75: 2516,
 79: 2517,
 83: 2518,
 108: 2520,
 116: 2531,
 125: 2532,
 122: 2533,
 149: 2534,
 137: 2535,
 156: 2827,
 157: 2537,
 176: 2546,
 187: 2547,
 191: 2549,
 1729: 2551,
 236: 2571,
 242: 2572,
 267: 2573,
 270: 2574,
 328: 2575,
 249: 2578,
 289: 2579,
 260: 2563,
 339: 2586,
 254: 2576,
 388: 2601,
 403: 2602,
 358: 2605,
 490: 2611,
 497: 2612,
 507: 2613,
 512: 2614,
 486: 2615,
 489: 2616,
 574: 2618,
 577: 2619,
 560: 2620,
 619: 2625}


crops_subgroup_list = [2656,2658,2655,2905,2919,2913,2911,2907,2909,2908,2912,2918,2922,2914]
start_year = 1961
end_year = 2013
yield_code = 5419
production_code = 5510
sugar_list_in_area_harvested = [2908,2922] #a list that has sugar subgroups for which average area production neeeds to be calculated
area_harvested_element_code = 5312
food_code = 5142

#codes in fbn
productions_code = 5511
imports_code = 5611
exports_code = 5911
domestic_code = 5301
feed_code = 5521

producing_animals_code = 5320
carcass_weight_code = 5417
livestock_yield_code = 5420
import_quantity_code = 5610
export_quantity_code = 5910
perm_pasture_code = 6655
temp_pasture_code = 6633
area_element_code = 5110
agriculture_land_code = 6610
stocks_code = 5111