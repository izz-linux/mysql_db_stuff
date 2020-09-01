#!/usr/bin/python3

# Written in Python 3.5.2
# Written by: Izz Noland
# Version 1.0.0 - 07/23/2018
"""
RELEASE NOTES
1.1.1 - Changed 2nd Saturday query to look at dashboardheader
1.1.0 - Changed criteria for progress to UpdatedDate
1.0.0 - Initial working version
0.5.0 - Initial tests
"""

import datetime
import base64
import mysql.connector
from dateutil.relativedelta import *
import sys


def getDashboardCounts(myCon, baSat):
    totalDashboards = 0

    cur = myCon.cursor()

    # If I set this to 11 in the getCurrentSaturday function, then I don't want to run it twice
    if baSat != 11:
        sql_query = 'select count(*) from dashboardconfig where generationfrequency = {} and includeindashboardgeneration = 1;'.format(baSat)

        # Open Connection and execute the query in sql script and store into the results array
        cur.execute(sql_query)
        # get initial count
        for i in cur:
            totalDashboards = i[0]

    #if isLastSaturday:
    #    sql_query = 'select count(*) from dashboardconfig where generationfrequency = 11 and includeindashboardgeneration = 1;'
    #    cur.execute(sql_query)

    #    for i in cur:
    #        totalDashboards += i[0]

    #if isNext2LastSaturday:
    #    sql_query = 'select count(*) from dashboardconfig where generationfrequency = 12 and includeindashboardgeneration = 1;'
    #    cur.execute(sql_query)

    #    for i in cur:
    #        totalDashboards += i[0]

    if isUpcomingLastSaturday:
        sql_query = 'select count(*) from dashboardconfig where generationfrequency = 11 and includeindashboardgeneration = 1;'
        cur.execute(sql_query)

        for i in cur:
            totalDashboards += i[0]

    if isUpcomingNext2LastSaturday:
        sql_query = 'select count(*) from dashboardconfig where generationfrequency = 12 and includeindashboardgeneration = 1;'
        cur.execute(sql_query)

        for i in cur:
            totalDashboards += i[0]

    cur.close()

    return totalDashboards


def getDashboardProgress(myCon, sat):
    # get the first day of the month
    d = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-01"), '%Y-%m-01')
    completedDashboards = 0

    cur = myCon.cursor()

    # I've changed this from createddate to updateddate
    #sql_query = "select count(*) from dashboardconfig where generationfrequency = {} and updateddate > '{}'".format(sat, d)

    sql_query = "select count(*) from dashboardheader where calendarmonth={} and calendaryear={} and createddate > '{}' " \
                "and createddate < '{}'".format(prevMonth,curYear,startWed,endTue)

    cur.execute(sql_query)

    for i in cur:
        completedDashboards += i[0]

    # special Saturdays
    if isUpcomingLastSaturday:
        sql_query = "select count(*) from dashboardconfig where generationfrequency = 11 and updateddate > '{}'".format(d)
        cur.execute(sql_query)

        for i in cur:
            completedDashboards += i[0]

    elif isUpcomingNext2LastSaturday:
        sql_query = "select count(*) from dashboardconfig where generationfrequency = 12 and updateddate > '{}'".format(d)
        cur.execute(sql_query)

        for i in cur:
            completedDashboards += i[0]

    return completedDashboards


# transform password function
def getPass(dec):
    # DN RO
    if dec == 1:
        b64txt = '***************'
        encodedtext = b64txt.encode()
        return base64.b64decode(encodedtext).decode()
    # Guess Who?
    elif dec == 2:
        b64txt = '***************'
        encodedtext = b64txt.encode()
        return base64.b64decode(encodedtext).decode()
    # UNKNOWN - Raise Exception
    else:
        raise ValueError("Who passed bad vars?! Schtanky!")


# get the current Saturday of the month
def getCurrentSaturday():
    # define globals and set to false for last and next to last Saturday
    global isLastSaturday
    global isNext2LastSaturday
    isLastSaturday = False
    isNext2LastSaturday = False

    d = datetime.datetime.strptime(datetime.datetime.now().strftime("%b %d, %Y"), '%b %d, %Y')

    if d == (d + relativedelta(day=31, weekday=SA(-1))):
        isLastSaturday = True
    elif d == (d + relativedelta(day=31, weekday=SA(-2))):
        isNext2LastSaturday = True

    # Confident this is correct for Saturdays 1 - 4 based on normal logic #
    if d.weekday() == 5 and 1 <= d.day <= 7:
        return 1
    if d.weekday() == 5 and 8 <= d.day <= 14:
        return 2
    if d.weekday() == 5 and 15 <= d.day <= 21:
        return 3
    if d.weekday() == 5 and 22 <= d.day <= 28:
        return 4
    if d.weekday() == 5 and 29 <= d.day <= 31:
        return 11

    return -1


def getUpcomingSaturday():
    global isUpcomingLastSaturday
    global isUpcomingNext2LastSaturday
    global startWed
    global endTue
    global prevMonth
    global curYear

    isUpcomingLastSaturday = False
    isUpcomingNext2LastSaturday = False

    d = datetime.datetime.strptime(datetime.datetime.now().strftime("%b %d, %Y"), '%b %d, %Y')
    t = datetime.timedelta((12 - d.weekday()) % 7)
    thisSat = d + t

    # added to work on dashboard progress
    startWed = thisSat - datetime.timedelta(days=3)
    endTue = thisSat + datetime.timedelta(days=3)
    prevMonth = d.month - 1
    curYear = d.year

    #print("The previous month is: {}\n".format(prevMonth))
    #print("The current year is: {}\n".format(curYear))


    if thisSat == (thisSat + relativedelta(day=31, weekday=SA(-1))):
        isUpcomingLastSaturday = True
    elif thisSat == (thisSat + relativedelta(day=31, weekday=SA(-2))):
        isUpcomingNext2LastSaturday = True

    # Confident this is correct for Saturdays 1 - 4 based on normal logic #
    if thisSat.weekday() == 5 and 1 <= thisSat.day <= 7:
        return 1
    if thisSat.weekday() == 5 and 8 <= thisSat.day <= 14:
        return 2
    if thisSat.weekday() == 5 and 15 <= thisSat.day <= 21:
        return 3
    if thisSat.weekday() == 5 and 22 <= thisSat.day <= 28:
        return 4
    if thisSat.weekday() == 5 and 29 <= thisSat.day <= 31:
        return 11

    return -1


# runLevel argument will be total / completed
def main(runLevl):
    # get decoded password
    decodedpwd = getPass(1)

    # setup connection to DN DB and run queries
    dnConnect = mysql.connector.connect(user='zbxExternal_ro', password=decodedpwd, host='rxdndb', database='datanet-3')

    #basicSat = getCurrentSaturday()
    basicSat = getUpcomingSaturday()
    if basicSat < 0:
        raise ValueError("Shit went bad, I don't know what Saturday it is!")

    if runLevel == "total":

        n = getDashboardCounts(dnConnect, basicSat)

        # close connection when done
        dnConnect.close()
        print(n)

    elif runLevel == "progress":
        n = getDashboardProgress(dnConnect, basicSat)
        # close connection when done
        dnConnect.close()
        print(n)

    else:
        # close connection when done
        dnConnect.close()
        raise ValueError("WTF Dude?! You put in a bad argument.  Use 'total' or 'progress'")


if __name__ == "__main__":
    main(sys.argv[1])
    #main()
