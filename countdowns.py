#! /usr/bin/env python

################################################################################
## Countdown.py
##
## This script reads a config file, and calculates the time to the events listed
## it prints, to stdout, the name of the event and the time to it, as specified
## in the confir file.
##
## To do
## ------------------------------------
## * create the 'event' as an object, not seperate variables
## * config file to read MUST be configurable
## * does the year wrap around?
## * create one off 'milestones' within the event (200 days, 100 days etc)
## * the shell markup "\033[1m;" MUST be configurable  
## * create some tests to run against this script
## * make it prettier
## * more useful comments
## * debug trace statements (toggle from command line?)
################################################################################
## BUGS
##
## 1) The runup date can be invalid. e.g. 31 march with 1 month runup = 31 feb << ERROR!
##   
################################################################################

from ConfigParser import ConfigParser
from datetime import date, timedelta

now=date.today()
#print str(now)

## Default values
##
## month : This month
## year  : This year
## freq  : annual
## runup : 1 month
parser=ConfigParser({'month':str(now.month), 'year':str(now.year),'frequency':'annual', 'runup':'1 month'})

config_fp=open('/home/jamie/bin/countdowns/countdowns.cfg')

parser.readfp(config_fp)

for event_name in parser.sections():
    #print "Processing event: " + event_name
    ###########################################################################
    #### Read the event information
    ###########################################################################
    next_occurance = None
    
    #print parser.items(event_name)
    event_day=parser.getint(event_name,'day')
    event_month=parser.getint(event_name, 'month')
    event_year=parser.getint(event_name, 'year')
    event_frequency=parser.get(event_name, 'frequency')
#    print "Event Freq : " + event_frequency
    event_date=date(event_year,event_month,event_day)
    #print "Event '" + event_name + "' date: " + event_date.strftime("%d %B %Y") + " freq: " + event_frequency
   
    #See if the date has already passed
    if event_date < now:
        #print "Date already passed. Looking for next one..."
        if 'once' == event_frequency:
            #print "once, so no next event"
            pass
        elif 'annual' == event_frequency:
            next_occurance=event_date.replace(year=now.year+1)
        elif 'monthly' == event_frequency:
            if event_month < 12:
                next_occurance=event_date.replace(month=now.month+1)
                #print "DEBUG: Month incremented"
            else:
                #print "Year wrap around - todo"
                next_occurance=event_date.replace(month=1,year=now.year+1)
    else:
        next_occurance=event_date

    if None != next_occurance:

        #print "next occurance = " + next_occurance.strftime("%d %B %Y")
  
## BUG: the runup date can be invalid. e.g. 31 march with 1 month runup = 31 feb << ERROR!
## So need to find a way around that.

        ## RUNUP
        runup=parser.get(event_name, 'runup')
        runup_value,runup_unit=runup.split()
        #print runup_value,runup_unit

        runup_value=int(runup_value)

        if runup_unit == 'year' or runup_unit == 'years':
            # TODO: annual runup
            pass
        elif runup_unit == 'month' or runup_unit == 'months':
            #print "processing month runup units"
            if next_occurance.month > 1: 
                runup_date=next_occurance.replace(month=next_occurance.month-runup_value)
            else:
               #print "next occurance is January, so need to fiddle a bit..." 
               runup_date=next_occurance.replace(month=13-runup_value, year=next_occurance.year-1)
        elif runup_unit == 'day' or runup_unit=='days':
            one_day = timedelta(days=1)
            runup_date=next_occurance - (runup_value * one_day)

        #print "Runup from :"  + runup_date.strftime("%d %B %Y")


        if now == event_date:
            print "It's \033[1m" + event_name + "\033[0m today!"
        else:
            if now > runup_date:
                countdown=abs(next_occurance - now)
                print "There are \033[1m" + str(countdown.days) + "\033[0m days 'til " + event_name
    #print "-" * 80

