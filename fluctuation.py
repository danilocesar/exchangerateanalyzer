#!/bin/env python

import sys
import datetime
import numpy

datelist = []

def run():
    process()

    print "Media Simples:"
    mediaSimples(1,31)

    print "Media Simples primeira Quinzena:"
    mediaSimples(1, 15)

    print "Media Simples segunda Quinzena:"
    mediaSimples(16, 31)

    print "Positivo X Negativo (Negativo->caiu mais vezes)"
    positivoXnegativo(1, 31)


def positivoXnegativo(start, end):
    results = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for obj in datelist:
        if (obj['date'].day >= start and obj['date'].day <= end):
            results[weekDay(obj)] += 1 if (obj['fluctuation'] >= 1.0000) else -1

    print 'Segunda ', results[0]
    print 'Terca   ', results[1]
    print 'Quarta  ', results[2]
    print 'Quinta  ', results[3]
    print 'Sexta   ', results[4]
    print "************************\n"

def mediaSimples(start, end):
    fluctuationXday = {0: [], 1: [], 2: [], 3: [], 4: []}

    for obj in datelist:
        if (obj['date'].day >= start and obj['date'].day <= end):
            fluctuationXday[weekDay(obj)].append(obj['fluctuation'])

    print 'Segunda ', numpy.mean(fluctuationXday[0])
    print 'Terca   ', numpy.mean(fluctuationXday[1])
    print 'Quarta  ', numpy.mean(fluctuationXday[2])
    print 'Quinta  ', numpy.mean(fluctuationXday[3])
    print 'Sexta   ', numpy.mean(fluctuationXday[4])
    print "************************\n"

def process():
    fileIN = open("exchange.data", "r")

    line = fileIN.readline().strip()

    limit = 30 * 12 * 10  # 10 years of limit
    if len(sys.argv) > 1:
        limit = int(sys.argv[1]) * 30 # limits in months

    while line:
        obj = createObjFromLine(line)
        datedelta = datetime.datetime.utcnow() - obj['date']

        if (datedelta.days < limit):
            appendToDateList(obj)

        line = fileIN.readline().strip()

def weekDay (obj):
    """
    return the weekDay from a obj with a datetime 'date' field
    weekDay 0 is monday
    """
    return obj['date'].weekday()

def createObjFromLine(line):
    """
    create an object containing
    {
        'date', which is a datetime object
        'rate', which is a float, showing the current exchange rate
    }

    where fluctuation is calculated from the last day
    """

    strdate, strvalue = line.split(' ')

    # Processing Date
    date = datetime.datetime.strptime(strdate, '%Y-%m-%d')
    value = float(strvalue)
    obj = {'date': date, 'value': value, 'fluctuation' : 1.0}
    return obj

def appendToDateList(obj):
    """
    * Append an object to the dateList
    * Adds a fluctuation member to the object, which is the
      variation from the day to the last day

    """
    fluctuation = 1.0
    if len(datelist) > 0:
        oldObj = datelist[-1]
        fluctuation =  obj['value'] / oldObj['value']

    obj['fluctuation'] = fluctuation

    datelist.append(obj)


try:
    run()
except Exception, e:
    print ("Error: " + str(e) + "")

