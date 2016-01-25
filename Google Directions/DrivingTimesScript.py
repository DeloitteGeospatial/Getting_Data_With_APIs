import googlemaps
import json
import csv
import datetime
from pprint import pprint

# Creates Google Maps object from API key

# John Tran's Key
##gmaps = googlemaps.Client(key='AIzaSyDIWatA967gBKF5sNGhGydb0XY-ExBKdkY')

# David's Key
gmaps = googlemaps.Client(key='AIzaSyBoORTHlDRQ2CRzQrssQfjT3r99xPJHjrE')

# Kevin's Key
##gmaps = googlemaps.Client(key='AIzaSyCUSkUaTU4DJhuheYoh3_x2y1BBD40N3yc')

# now = datetime.now()

t = datetime.time(8, 30, 0)

d = datetime.date.today()

dt = datetime.datetime.combine(d, t)

print (dt)

# Creates array of employee zip codes

zips = []
oids = []
states = []

fname = 'C:/TravelTimes/TravelTimesResult3.csv'
texta = 'OID,Raw Input,Driving Time to Bethlehem in minutes,Driving Time to Cranford Train Station'
texta = texta + '\n'

with open('C:/TravelTimes/EmployeesF.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tempAr = []
        zips.append(row['Raw Input'])
##        zips.append(row['Employee Residence'])
        oids.append(row['OID'])
        




destinations = ['6255 Sterners Way, Bethlehem, PA, 18017','40.655702, -74.303248']

# Request public transit directions via Google Maps API

count = 0

for zp in zips:
    origin = zp
##    
##    o = origin.replace(","," ")
##
##    city = o[:len(o) - 10]
##    print city
##    
##    state = o[len(o) - 8:len(o) - 6]
##    zipc = str(o[len(o) - 5:]).zfill(5)
##    print state
##    print zipc
    
##    texta = texta + str(count) + "," + o + "," + city + "," + state + "," + str(zipc).zfill(5) + ","
    texta = texta + str(oids[count]) + "," + str(zp)
    
    for ds in destinations:
        destination = ds

        directions_result = gmaps.directions(origin,
                                             destination,
                                             mode="driving")

        dictio = directions_result[0]
        leg = (dictio['legs'])

        a = leg[0]

##        pprint (dictio)
##        print ("")
##        print ("")
##        pprint (leg)
##        print ("")
##        print ("")
##        pprint (a)

        durlist = a['duration']

        durtext = durlist['text']

        duration = durtext.replace(" mins","")
        duration = duration.replace(" min","")

##        print (duration)

        x = 'hours'

        nduration = ''

        if x in duration:
            xind = duration.index(x)
            hoursub = duration[:xind]
##            print hoursub
            time = int(hoursub) * 60
            minsub = duration[(xind + 6):]
##            print minsub
            nduration = int(time) + int(minsub)

        y = 'hour'
        
        if y in duration and x not in duration:
            xind = duration.index(y)
            hoursub = duration[:xind]
##            print hoursub
            time = int(hoursub) * 60
            minsub = duration[(xind + 5):]
##            print minsub
            nduration = int(time) + int(minsub)

        if y not in duration and x not in duration:
            nduration = int(duration)

        texta = texta + "," + str(nduration)

    count = count + 1
    texta = texta + "\n"


        # Grab relevant info from query results

##        if directions_result <> []:
##            
##            dictio = directions_result[0]
##            
##            leg = (dictio['legs'])
##            a = leg[0]
##
##            distlist = a['distance']
##            distance = distlist['text']
##            distm = distlist['value']
##
##            durlist = a['duration']
##
##            # pprint(a)
##
##            # Converts query results to int
##
##            if 'departure_time' in a.keys():
##
##                depart = a['departure_time']
##                departtime = depart['text']
##
##                loc1 = departtime.index(":")
##                prefix = departtime[loc1+3]
##                loc2 = departtime.index(prefix)
##
##                dhour = int(departtime[:loc1])
##                dmin = int(departtime[(loc1+1):loc2])
##
##                arrive = a['arrival_time']
##                arrivetime = arrive['text']
##
##                loc1 = arrivetime.index(":")
##                prefix2 = arrivetime[loc1+3]
##                loc2 = arrivetime.index(prefix2)
##
##                ahour = int(arrivetime[:loc1])
##                amin = int(arrivetime[(loc1+1):loc2])
##
##                # Calculate travel time
##
##                traveltime = 0
##
##                if dhour == ahour:
##                    traveltime = amin - dmin
##                elif (prefix == prefix2 and dhour == 12):
##                    traveltime = (ahour * 60) + amin - dmin
##                elif (prefix == prefix2 and dhour <> 12):
##                    traveltime = ((ahour - dhour)*60) + amin - dmin
##                elif ((prefix <> prefix2) and (ahour == 12)):
##                    traveltime = ((12 - dhour)*60) + amin - dmin
##                elif ((prefix <> prefix2) and (ahour <> 12)):
##                    traveltime = ((12 - dhour)*60) + 60 + amin - dmin
##
##                # Print results
##
##                texta = texta + str(distance).replace(" mi", "") + "," + str(traveltime) + ","
##            
##
##            else:
##                texta = texta + str(distlist['text']).replace(" mi", "") + "," + str(durlist['text']).replace(" mins","") + ","
##
##        elif directions_result == []:
##            print ("No transit available for trip")
##            texta = texta + "N/A,N/A,"
##            print (origin + " to " + destination)
##    texta = texta + "\n"
##    count = count + 1

# Write to file

    m = open(fname, 'w')
    m.write(texta)
    m.close()
        

