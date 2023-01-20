# permit_finder
A basic script to search the Philadelphia building and zoning permit info for a keyword. 
Created because I needed to check if a contractor had filed for a permit, and see if it was delayed, because it wasn't showing up [on Atlas.](https://atlas.phila.gov/)

Philly permits we assumed to be of the format:  Type-Year-XXXXXX (e.g. RP-2022-002377).
Some types of permits and their prefix include:
- RESIDENTIAL BUILDING PERMIT    (RP)
- ZONING PERMIT    (ZP)
- PLUMBING PERMIT (PP)
- GENERAL PERMIT (GP)
- ELECTRICAL PERMIT (EP)

- VIOLATION CASE (CF)

However, older permits may only be numbers (e.g. 59304). I have no idea what year the numbering syste switched over, because I was only looking for recent permits.

## Requirements  
Because of how the content is generated, this script uses selenium to scrape the data from the 

- Python 3.9.7
- numpy
- argparse
- tqdm
- selenium

## Use

-k --keyword  : What keyword you want to search for. I usually use the street name
-p --permit : Type of permit to start with (e.g. RP-2022-001000)
-l --length : How many consecutive permits to search, default is 10

Frequently, the website lags and the data is not found. Or the permit number is invalid. These cases are stored and can be displayed at the end of the search. 

```python
python permit_finder.py -k Powelton -l 20 -p RP-2022-001001

Searching...:   0%|                                               | 0/20 [00:00<?, ?it/s]Found Permit: RP-2022-001001
LOCATION
4023 POWELTON AVE
APPLICATION DESCRIPTION
RESIDENTIAL BUILDING PERMIT
STATUS
ISSUED
COMMENTS
ALL APPLICABLE REVIEWS HAVE BEEN APPROVED AND PERMIT FEES PAID.
APPLICATION SUBMISSION DATE
Friday, January 28th 2022
DUE DATE OF LATEST REVIEW
Wednesday, February 2nd 2022
DATE REVIEW COMPLETED
Wednesday, February 2nd 2022
Searching...: 100%|████████████████████████████████████████████████████████████████| 20/20 [02:32<00:00,  7.64s/it]

 ******  ******  ******  ******
Completed search of 20 permits: RP-2022-001001 to RP-2022-001020

These 1 permits found with keyword:POWELTON
RP-2022-001001
13 SKIPPED during search due to errors
Display skipped? [y / n]  n
```
