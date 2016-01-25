__author__ = 'kdenny'

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]




def getACS_base(outLoc,inStates):
    ## Title: Census Bureau American Community Survey (ACS) API Automated Query Script
    ## Written By: Kevin Denny, Deloitte
    ## Support: kdenny@deloitte.com
    ##
    ## Description: Given a .csv file containing a list of names and table titles of ACS data fields, this script automatically queries the Census Bureau's API
    ## and populates data files for the provided data fields across every Census tract in the U.S. This script requires an API key from the Census Bureau and
    ## the Census Python package (available at https://pypi.python.org/pypi/census)

    ######################################################################################################################################################

    from census import Census
    from us import states
    import csv
    import os
    from datetime import datetime


    c = Census("fc35b71dfc10725453726fd1e8bcb1c6063db66f")

    ##c = Census("YOUR KEY HERE") ### A key can be obtained at http://api.census.gov/data/key_signup.html

    fipsLoc = 'C:\Users/kdenny/Documents/PostalSegmentation/Params/fips_codes.csv'
    dataLoc = 'C:\Users/kdenny/Documents/SegmentrWorking/Params/dataFieldsI.csv'

    indic = 'SegmentIndicators' ## This is the name of the .csv file you will create for each county; update for each different type (e.g. Economic, Housing)
    opath = outLoc + 'DataFiles/'

    # print ("Do you wish to overwrite existing ACS files? ")
    # overwrite = raw_input("(Y/N) ")
    # ow = overwrite.upper()


    datum = []
    datumNames = []
    allData = []
    allFields = ['State', 'Tract', 'County']
    ## Dictionary of all data field metadata, with the Datum Name as the key
    datumDict = {}

    statesCounties = []

    # print ("Start")
    # print (datetime.now().time())

    ## Populate list of states and counties

    with open(fipsLoc) as csvfile:
        reader = csv.DictReader(csvfile)
        for b in inStates:
            for row in reader:
                tempAr = []
                curState = str(row['State FIPS Code'])
                # if curState == b:
                tempAr.append(str(row['State FIPS Code']))
                tempAr.append(str(row['County FIPS Code']))
                if (tempAr not in statesCounties):
                    statesCounties.append(tempAr)
    # print(statesCounties)

    ## Populate list of datum fields / datum names

    with open(dataLoc) as csvfile2:
        reader2 = csv.DictReader(csvfile2)
        for rowa in reader2:
            datumDict[rowa['DatumName']] = rowa
            datum.append(str(rowa['TableID']))
            datumNames.append(str(rowa['DatumName']))

    # Creates any necessary folders / subfolders
    # vars = {
    finStates = []
    finCounties = []
    for ss in inStates:
        path = opath
        if not os.path.exists(path):
            os.makedirs(path)
        fname = path + str(ss) + 'DataFields.csv'

        # print(datetime.now().time())
        # print(fname)
        # print ("")
        texta = ''
        textb = ''
        if (os.path.isfile(fname) == False):
            # os.remove(fname)
            # if not os.path.isfile(fname):
            textb = textb + 'State,County,Tract'
            k = 0
            # while k < len(datum):
            #     textb = textb + ',' + datumNames[k]
            #     k = k + 1
            for k in datumDict:
                ag = datumDict[k]
                textb = textb + ',' + ag['DatumName']

            textb = textb + '\n'
            # n = open(fname, 'w')
            # n.write(textb)
            # n.close()

        # Begin creating data file for county
            data = {}
            for sd in statesCounties:
                texta = ''
                allVars = {}
                if  int(sd[0]) == int(ss):
                    state = str(sd[0]).zfill(2)
                    county = str(sd[1]).zfill(3)
                    statecounty = str(state) + str(county)

                    if county != '000':

                        # Process tracts
                        l = 0
                        for dName in datumDict:
                            # print dName
                            datumRow = datumDict[dName]
                            # print(datumRow)
                            tid = str(datumRow['TableID']).strip()
                            co = int(datumRow['OID']) - 1
                            # print tid
                            # print state
                            # print county
                            if (tid != 'ADD'):
                                aString = c.acs.state_county_tract(tid, state, county, Census.ALL)
                                pid = datumRow['Percentof'].strip()
                                if pid.strip() != '' and pid.strip() != 'FIX' and pid.strip() != 'N/A':
                                    div = c.acs.state_county_tract(pid, state, county, Census.ALL)
                                # print(aString)
                                result = aString

                                if (result != []):
                                    i = 0
                                    for atta in result:
                                        # print atta[tid]
                                        di = div[i]
                                        if pid != 'FIX' and pid != 'N/A':
                                            if (atta[tid].isnumeric()):
                                                if (di[pid].isnumeric()):
                                                    if float(di[pid]) != 0:
                                                        atta[tid] = float(float(atta[tid]) / float(di[pid]))
                                        result[i] = atta
                                        i = i + 1

                                allVars[dName] = result





                            elif ((datumRow['TableID']).strip() == 'ADD'):
                                aString = datumRow['Together']
                                pluses = find(aString,'+')
                                fields = []
                                cresult = 0
                                i = 0
                                for pl in pluses:
                                    field = aString[i:pl]
                                    i = pl + 2
                                    cString = c.acs.state_county_tract(field, state, county, Census.ALL)
                                    if (cString != []):
                                        if cString.isnumeric():
                                            cresult += cString
                                result = cresult
                                # allVars.append(result)

                            data[statecounty] = allVars


                    # print ("Done processing tracts for" + state + ", " + county)
                    # print allVars
                    # print (datetime.now().time())

                    tracts = []

                    a = 0
                    listOfVars = {}

                    # Cleans up data results

                    for vark in allVars:
                        tempList = []
                        # print (vark)
                        name = ''
                        for key in allVars[vark][0]:
                            if key != u'county' and key.replace("u","") != 'tract' and key.replace("u","") != 'state':
                                name = key.replace("u","'")
                        for s in allVars[vark]:
                            if a == 0:
                                tr = s['tract'].replace("u","")
                                tracts.append(str(tr).zfill(6))

                            md = s[name]
                            tempList.append(md)
                            # print ("tttt")
                            if md == 'None':
                                tempList.append('0')
                            # print (tempList)
                        # listOfVars.append(tempList)
                        listOfVars[vark] = tempList
                        a = a + 1

                        f = 0

                    # Writes API query results as a string

                    for d in tracts:
                        dataG = {}

                        dataG['Tract'] = str(tracts[f]).zfill(6)
                        dataG['State'] = state
                        dataG['County'] = county
                        texta = texta + state + "," + county + "," + str(tracts[f]).zfill(6)
                        line = state + "," + county + "," + str(tracts[f]).zfill(6)
                        # print line
                        g = 0
                        for m in listOfVars:
                            vList = listOfVars[m]
                            texta = texta + "," + str(vList[f])
                            dataG[m] = vList[f]
                            g = g + 1
                        f = f + 1
                        # print (texta)
                        texta = texta + "\n"
                        allData.append(dataG)

            for key in datumDict:
                allFields.append(key)
            # dr.fieldnames contains values from first row of `f`.
            with open(fname,'wb') as fou:
                dw = csv.DictWriter(fou, delimiter=',', fieldnames=allFields)
                print (allFields)
                headers = {}
                for n in dw.fieldnames:
                    headers[n] = n
                dw.writerow(headers)
                for row in allData:
                    print row
                    dw.writerow(row)
            fou.close()
            print ("ACS Data gathered for ") + str(ss)
            # Exports results string to the identified output file
            #     print texta
            #     m = open(fname, 'a')
            #     # print fname
            #     # print texta
            #     m.write(texta)
            #     m.close()


        elif (os.path.isfile(fname)):
            return



getACS_base(r"C:\Users\kdenny\Documents\SegmentrWorking\SegmentrTest", ['11'])