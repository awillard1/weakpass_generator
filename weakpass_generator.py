#!/usr/bin/env python3
# 2020.02.18 - @nyxgeek - TrustedSec
# 2020.02.28 - @awillard1 - aswsec
# TODO: REFACTOR again
# generate weak passwords based on current date
import holidays, string
import re
import datetime
from datetime import datetime, timedelta

hcnty= ['AR','AW','AU','AT','BY','BE','BR','BG','CA','CL','CO','HR','CZ','DK','DO','EG','EE','ECB','FI','FRA','DE','GR','HND','HK','HU','IS','IND','IE','IL','IT','JP','KE','LT','LU','MX','NL','NZ','NI','NG','NO','PY','PE','PL','PT','PTE','RU','RS','SG','SK','SI','ZA','ES','SE','CH','UA','UK','US']
#Define our Months and Keywords for Prefixes
monthDictionary = {}
monthDictionary["January"] = ["January", "Winter"]
monthDictionary["February"] = ["February", "Winter"]
monthDictionary["March"] = ["March", "Winter", "Spring"]
monthDictionary["April"] = ["April", "Spring"]
monthDictionary["May"] = ["May", "Spring", "Summer"]
monthDictionary["June"] = ["June", "Spring","Summer"]
monthDictionary["July"] = ["July", "Summer"]
monthDictionary["August"] = ["August", "Summer", "Fall", "Autumn"]
monthDictionary["September"] = ["September", "Fall", "Autumn"]
monthDictionary["October"] = ["October", "Fall", "Autumn", "Winter"]
monthDictionary["November"] = ["November", "Fall", "Autumn", "Winter"]
monthDictionary["December"] = ["December", "Winter"]

OUTPUT_LIST = []

p = re.compile('[^a-zA-Z0-9]')

def checkIfDuplicate(listOfElems,item):
    for elem in listOfElems:
        if elem==item:
            return True
    return False

def createSuffixArray(tempdate):
    year_short=tempdate.strftime("%y")
    year_long=tempdate.strftime("%Y")
    suffix_array = [year_short, year_long, "1", "123"]
    #Use this to simplify using special characters
    #loop through them and add to the array
    for c in string.punctuation:
        suffix_array.append(c+year_short)
        suffix_array.append(c+year_long)
        suffix_array.append(year_short+c)
        suffix_array.append(year_long+c)
    return suffix_array    
    
def createMonthDictionary(tempdate):
    current_month=tempdate.strftime("%B")
    for cntry in hcnty:
        hdays = holidays.CountryHoliday(cntry)
        tempholiday = hdays.get(tempdate.strftime("%Y-%m-%d"))
        subholiday = ""
        preholiday = ""
        if tempholiday:
            i = 0
            e = 0
            #Remove the word observed
            tempholiday = tempholiday.replace('(Observed)','')
            if tempholiday.find('(') > 0:
                i=tempholiday.index('(')
                e=tempholiday.index(')')
            elif tempholiday.find('[') > 0:
                i = tempholiday.index('[')
                e = tempholiday.index(']')
            if i > 0:
                subholiday = tempholiday[i+1:e].strip()
                preholiday = tempholiday[0:i].strip()
            
            if len(subholiday) > 0:
                shold = p.sub('',subholiday)
                if False == checkIfDuplicate(monthDictionary[current_month], shold):
                    monthDictionary[current_month].append(shold)
            if len(preholiday) > 0:
                phold = p.sub('',preholiday)
                if False == checkIfDuplicate(monthDictionary[current_month], phold):
                    monthDictionary[current_month].append(phold)
                    
            h = p.sub('',tempholiday)
            if False == checkIfDuplicate(monthDictionary[current_month],h):
                monthDictionary[current_month].append(h)
            
            if h.endswith('Day'):
                h = h.replace('Day','').strip()
                if False == checkIfDuplicate(monthDictionary[current_month],h):
                    monthDictionary[current_month].append(h)

def create_passwords(tempdate):
    current_month=tempdate.strftime("%B")
    createMonthDictionary(tempdate)
    SUFFIX_ARRAY = createSuffixArray(tempdate)
    for month_prefix in monthDictionary[current_month]:
        for password_suffix in SUFFIX_ARRAY:
            #print("%s%s" % (month_prefix, password_suffix) )
            global OUTPUT_LIST
            OUTPUT_LIST.append("%s%s" % (month_prefix, password_suffix))


for numberofdays in range(1,180):
    tempdate = datetime.now() - timedelta(days=numberofdays)
    create_passwords(tempdate)


#print the unique ones
print("Here are the results:")

OUTPUT_LIST.sort()
output_set = sorted(set(OUTPUT_LIST))

#open file to write to
outfile = open("latest_passwords.txt", "w")


#iterate through our sorted and uniqued list
for candidate_password in output_set:
    print(candidate_password)
    outfile.write(candidate_password+"\n")


#close our file now
outfile.close()
