Here is a step-by-step instruction for setup:

1) Download all the .csv files from the following Google Drive link:

https://drive.google.com/drive/folders/1zEExlrY4L9FLnCE7PZl73dTxSCX9PN8z?usp=sharing

2) Save all the csvs in the same folder as master folder (i.e the folder of which contains this README file)

3) Assure that the python package of pandas is installed. Here is the link for it: https://pandas.pydata.org

4) Work with the python file - run.py for generating land-spared vs years results for food group - continent pairs. Instructions on how to do that is provided in run.py. A sample python notebook named test.ipynb (included in master) is also included for better understanding of some/all functions in dietary_faotools.py and var_dietary_faotools.py. 

5) dietary_faotools.py contains functions that evaluate land related functions according to the USDA diet recommendation of 2010. var_faotools.py contains functions that evaluate land related functions according to arbitrary diet distributions in populations.

6) Work with the python file - run_country.py for generating land-spared vs years results for food-group-country pairs.  Instructions on how to do that is provided in run_country.py. 

DOI badge the project:

https://zenodo.org/badge/DOI/10.5281/zenodo.3353631.svg

DOI:

10.5281/zenodo.3353631


Technical Notes:

1) When running temporal results for countries from run_country.py please note that countries like Yugoslavia and USSR do not exist after 1991 and so the all results for them is 0 after those years. Similarly, Serbia, Croatia etc (all countries breaking up from Former Yugoslavia) and Russia do not exist before 1991 and so all the results for those country codes are 0 after that date. To observe the temporal results (1961-2013) of the geopolitical region of, let's say present day Croatia, you have to observe the results of Yugoslavia (normalized by the population of Croatia region in Yugoslavia) till 1991 and observe the results of Croatia from 1991 onwards.

