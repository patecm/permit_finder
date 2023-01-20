#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes arguments:
    --keyword : Word to search permit sit for. Recommend using street name.
    --permit : Permit to start search wtih
    --search_length : How many consecutive permits to search
"""

import numpy as np
import time
import argparse
from tqdm import tqdm


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# RP-2022-012350

parser = argparse.ArgumentParser(
                    prog = 'PermitLookup',
                    description = 'Checks blocks of Philly Atlas permis')
#parser.add_argument('filename')           # positional argument
parser.add_argument('-k', '--keyword', dest='keyword',)
parser.add_argument('--permit' , '-p')
parser.add_argument('-l', '--length', dest='length', default=10, type=int,
                    help='Number of permits to search (optional). Default=10')
parser.add_argument('-s', '--stop', dest='stopage', action='store_true')
args = parser.parse_args()

# ## Process permit formatting ## #
permit_parts = args.permit.split('-')
suffix_length = len(permit_parts[-1])
initial_suffix = int(permit_parts[-1]) #strips leading zeros
    
# ## Function to setup selenium browser and fetch a single record ## #
# input: permit_number, number of attempts upon exception
def GetRecord(permit_number, exceptions=1):
    #print(f'Checking {permit_number}')
    s=Service('/Users/cassandrapate/Documents/chromedrivers/chromedriver108')
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--verbose")
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(f'https://www.phila.gov/li-permit-tracker/?id={permit_number}')
    time.sleep(3) # pause to not get blocked

    try:
        input_elements = driver.find_element(by=By.ID, value="application-details")
        application_text = input_elements.text
    except NoSuchElementException:
        driver.quit()
        application_text = 'None'
        if exceptions > 0:
            #print(f'...Exception on {permit_number} | trying again')
            exceptions -= 1
            GetRecord(permit_number, exceptions=exceptions)
        #else:
            #print(f'Out of attempts. Skipping {permit_number}.')
            
    driver.quit()
    #input_elements =  WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'application-details')))
    return(application_text)

# ## Cycle through permits ## #

skipped_permits = []
keyword_permits = []

# for current_suffix in np.arange(initial_suffix, initial_suffix+args.length):
for current_suffix in tqdm(range(initial_suffix, initial_suffix+args.length), desc='Searching...'):

    zero_padding = '0' * (len(permit_parts[-1]) - len(str(current_suffix)))
    full_permit = '-'.join([permit_parts[0], permit_parts[1], zero_padding+str(current_suffix)])
    
    # Fetch permit record
    application_text = GetRecord(full_permit, exceptions=1)
    
    # Save matching permits
    if args.keyword.upper() in application_text:
        print(f'Found Permit: {full_permit}')
        print(application_text)
        keyword_permits.append(full_permit)
        
    # Handle permits skipped or missing
    if 'None' in application_text:
        skipped_permits.append(full_permit)
    
    #time.sleep(1) #pause again to not overwhelm server


# ## Text to display at end ## #
print('\n ******  ******  ******  ******')
print(f'Completed search of {args.length} permits: {args.permit} to {full_permit}\n')
if len(keyword_permits) > 0:
    print(f'These {len(keyword_permits)} permits found with keyword:{args.keyword.upper()}')
    for p in keyword_permits: print(p)
else:
    print(f'No permits fround with keyword: {args.keyword.upper()}\n')
    
print(f'{len(skipped_permits)} SKIPPED during search due to errors')
if len(skipped_permits) > 0:
    display_skipped = input('Display skipped? [y / n]  ')

if 'y' in display_skipped.lower():
    for p in skipped_permits: print(p)